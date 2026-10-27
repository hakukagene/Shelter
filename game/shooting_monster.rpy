init python:
    import math
    import time

    SHOOTING_MONSTER_FRAMES = [
        Transform("images/shooting_test/monster/monster-%02d.png" % index, xysize=(720,720))
        for index in range(8)
    ] + [
        Transform("images/shooting_test/monster/claw-%02d.png" % index,xysize=(720,720),
                xzoom=-1 if index in (4,6) else 1)
        for index in range(8)
    ]
    SHOOTING_MONSTER_STRIKE_FPS = 25
    SHOOTING_MONSTER_STRIKE_TIMELINE = (0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7)
    SHOOTING_MONSTER_CONTACT_TICKS = (6,18)
    SHOOTING_DOOR_MAX_HP = 100
    SHOOTING_MONSTER_DAMAGE = 10
    SHOOTING_MONSTER_BODY_DAMAGE = 1.0
    SHOOTING_MONSTER_HEAD_DAMAGE = 1.5
    SHOOTING_MONSTER_BLOOD_FRAMES = [
        Transform("images/shooting_test/blood/blood-%02d.png" % index,xysize=(160,160))
        for index in range(8)
    ]
    SHOOTING_MONSTER_BLOOD_DURATION = 8/25.0
    # Trapezoid traced from the user's marked street area in logical pixels.
    # Both movement and debug paths derive their floor depth from this shape.
    SHOOTING_MONSTER_ROAD = ((855,550),(1060,550),(1900,1000),(20,1000))
    SHOOTING_MONSTER_LANES_FAR = (885,960,1035)
    SHOOTING_MONSTER_LANES_NEAR = (610,970,1420)
    SHOOTING_MONSTER_ROUTE_NAMES = ("Зүүн", "Гол", "Баруун")
    SHOOTING_MONSTER_NEAR_HEAD = 316
    # Logical pixels in the supplied door art: draw the creature only through
    # the glass panes, leaving the door, mullions and locking wheel in front.
    SHOOTING_MONSTER_PANES = tuple(
        (left,top,right-left,bottom-top)
        for left,right in ((241,389),(423,709),(739,1183),(1211,1492),(1527,1685))
        for top,bottom in ((117,211),(244,609))
    )
    renpy.music.register_channel("shooting_test_monster", mixer="sfx", loop=False)

    class ShelterMonsterPaneMask(renpy.Displayable):
        def render(self,width,height,st,at):
            result = renpy.Render(1920,1080)
            canvas = result.canvas()
            for rectangle in SHOOTING_MONSTER_PANES:
                canvas.rect((255,255,255,255),rectangle)
            return result

    class ShelterMonsterDebugRoad(renpy.Displayable):
        def __init__(self,monster):
            super(ShelterMonsterDebugRoad,self).__init__()
            self.monster = monster
            self.route_key = None
            self.refresh()

        def refresh(self):
            key = (self.monster.route_index,self.monster.lane_changes,SHOOTING_MONSTER_ROAD)
            if key != self.route_key:
                self.routes = [tuple(self.monster.geometry_at_progress(index/100.0,route)[:2]
                                    for index in range(101)) for route in range(3)]
                self.route_key = key
                renpy.redraw(self,0)

        def per_interact(self):
            self.refresh()

        def render(self,width,height,st,at):
            result = renpy.Render(1920,1080)
            canvas = result.canvas()
            points = SHOOTING_MONSTER_ROAD
            for first,second in zip(points,points[1:]+points[:1]):
                canvas.line((50,240,110,255),first,second,3)
            for index,route in enumerate(self.routes):
                color = (80,230,255,255) if index == self.monster.route_index else (70,145,215,160)
                for first,second in zip(route,route[1:]):
                    canvas.line(color,first,second,3 if index == self.monster.route_index else 1)
                canvas.circle(color,route[-1],5)
            return result

    class ShelterDoorHealth(object):
        def __init__(self):
            self.hp = SHOOTING_DOOR_MAX_HP
            self.impacts = 0
            self.kills = 0

    class ShelterMonsterCrowd(renpy.Displayable):
        def __init__(self,owner):
            super(ShelterMonsterCrowd,self).__init__()
            self.owner = owner

        def visit(self):
            return self.owner.monsters

        def render(self,width,height,st,at):
            result = renpy.Render(1920,1080)
            now = time.perf_counter()
            for monster in sorted(self.owner.monsters,key=lambda item:item.geometry(now)[1]):
                result.blit(renpy.render(monster,1920,1080,st,at),(0,0))
            renpy.redraw(self,.04)
            return result

    class ShelterDoorMonster(renpy.Displayable):
        approach_duration = 4.0
        windup_duration = .20
        strike_duration = len(SHOOTING_MONSTER_STRIKE_TIMELINE)/25.0
        strike_beat = strike_duration/2.0

        def __init__(self,door=None,auto_respawn=True,**kwargs):
            super(ShelterDoorMonster,self).__init__(**kwargs)
            self.door = door if door is not None else ShelterDoorHealth()
            self.auto_respawn = auto_respawn
            self.route_index = -1
            self.approach_count = 0
            self.death_frames = [Transform(SHOOTING_MONSTER_FRAMES[8],alpha=(8-index)/8.0)
                                for index in range(9)]
            self.restart(delay=1.2)
            # Reuse a fixed set of transforms; brightness changes on the GPU,
            # without making additional PNGs or per-frame displayables.
            self.lit_frames = [Transform(frame,function=self.light_transform)
                            for frame in SHOOTING_MONSTER_FRAMES]
            self.lit_death_frames = [Transform(frame,function=self.light_transform)
                                    for frame in self.death_frames]

        @property
        def door_hp(self):
            return self.door.hp

        @door_hp.setter
        def door_hp(self,value):
            self.door.hp = value

        @property
        def impacts(self):
            return self.door.impacts

        @impacts.setter
        def impacts(self,value):
            self.door.impacts = value

        @property
        def kills(self):
            return self.door.kills

        @kills.setter
        def kills(self,value):
            self.door.kills = value

        def restart(self,delay=0,route=None,changes=None):
            now = time.perf_counter()
            self.route_index = (self.route_index+1)%3 if route is None else int(route)%3
            self.approach_count += 1
            self.lane_changes = (2 if self.approach_count%2 else 3) if changes is None else max(2,min(3,int(changes)))
            self.completed_changes = 0
            self.state = "waiting"
            self.approach_started = now+delay
            self.strike_started = 0
            self.windup_started = 0
            self.next_impact = float("inf")
            self.strike_impact_index = 0
            self.last_impact_hand = None
            self.impact_until = 0
            self.hit_until = 0
            self.respawn_at = 0
            self.hp = 3
            self.last_hit_zone = None
            self.blood_events = []
            self.breach_geometry = None
            renpy.music.stop(channel="shooting_test_monster")
            renpy.redraw(self,0)

        def visit(self):
            return self.lit_frames+self.lit_death_frames+SHOOTING_MONSTER_BLOOD_FRAMES

        def light_at(self,now):
            progress = max(0,min(1,(now-self.approach_started)/self.approach_duration))
            depth = progress*progress*(3-2*progress)
            return .10+.90*depth

        def light_transform(self,transform,st,at):
            light = self.light_at(time.perf_counter())
            transform.matrixcolor = TintMatrix(Color(rgb=(light,light,light)))
            return .04

        def blood_size(self,size):
            return max(60,min(264,size*.44))

        def geometry(self,now):
            if self.state == "breached" and self.breach_geometry is not None:
                return self.breach_geometry
            progress = max(0,min(1,(now-self.approach_started)/self.approach_duration))
            return self.geometry_at_progress(progress)

        def lane_plan(self,route=None,changes=None):
            route = self.route_index if route is None else int(route)%3
            changes = self.lane_changes if changes is None else changes
            if changes == 2:
                lanes = ((0,1,0),(1,0,1),(2,1,2))[route]
                times = (0,.40,.84)
            else:
                lanes = ((1,2,1,0),(0,1,2,1),(1,0,1,2))[route]
                times = (0,.28,.56,.84)
            return tuple(zip(times,lanes))

        def geometry_at_progress(self,progress,route=None,changes=None):
            progress = max(0,min(1,progress))
            route = self.route_index if route is None else int(route)%3
            depth = progress*progress*(3-2*progress)
            plan = self.lane_plan(route,changes)
            lane_from = lane_to = plan[-1][1]
            mix = 0
            for first,second in zip(plan,plan[1:]):
                if progress < second[0]:
                    lane_from,lane_to = first[1],second[1]
                    mix = (progress-first[0])/(second[0]-first[0])
                    mix = mix*mix*(3-2*mix)
                    break
            far = SHOOTING_MONSTER_LANES_FAR
            near = SHOOTING_MONSTER_LANES_NEAR
            start_x = far[lane_from]+(near[lane_from]-far[lane_from])*depth
            end_x = far[lane_to]+(near[lane_to]-far[lane_to])*depth
            x = start_x+(end_x-start_x)*mix
            far_y = (SHOOTING_MONSTER_ROAD[0][1]+SHOOTING_MONSTER_ROAD[1][1])/2.0
            near_y = (SHOOTING_MONSTER_ROAD[2][1]+SHOOTING_MONSTER_ROAD[3][1])/2.0
            foot = far_y+(near_y-far_y)*depth
            head = far_y-72+(SHOOTING_MONSTER_NEAR_HEAD-(far_y-72))*depth
            return x,foot,foot-head

        def frame_at(self,now):
            if self.state == "breached":
                return 10 if self.last_impact_hand == "left" else 14
            if self.state == "windup":
                return 8
            if self.state == "strike":
                tick = int(math.floor(max(0,now-self.strike_started)*25+1e-8)) % len(SHOOTING_MONSTER_STRIKE_TIMELINE)
                return 8+SHOOTING_MONSTER_STRIKE_TIMELINE[tick]
            elapsed = max(0,min(self.approach_duration,now-self.approach_started))
            braking = max(0,elapsed-(self.approach_duration-.8))
            stride = elapsed*12.5-12.5*braking*braking/(2*.8)
            return int(stride) % 8

        def advance(self,now):
            changed = False
            self.blood_events = [event for event in self.blood_events
                                if now-event[0] < SHOOTING_MONSTER_BLOOD_DURATION]
            if self.door_hp <= 0:
                if self.state not in ("gone","breached"):
                    self.breach_geometry = self.geometry(now)
                    self.state = "breached"
                    self.next_impact = float("inf")
                    changed = True
                renpy.redraw(self,0)
                return changed
            if self.state == "waiting" and now >= self.approach_started:
                self.state = "approach"
                changed = True
            if self.state == "approach" and now >= self.approach_started+self.approach_duration:
                self.state = "windup"
                self.windup_started = self.approach_started+self.approach_duration
                changed = True
            if self.state in ("approach","windup"):
                progress = max(0,min(1,(now-self.approach_started)/self.approach_duration))
                completed = sum(progress >= phase for phase,lane in self.lane_plan()[1:])
                if completed != self.completed_changes:
                    self.completed_changes = completed
                    changed = True
            if self.state == "windup" and now >= self.windup_started+self.windup_duration:
                self.state = "strike"
                self.strike_started = self.windup_started+self.windup_duration
                self.strike_impact_index = 0
                self.next_impact = self.strike_started+SHOOTING_MONSTER_CONTACT_TICKS[0]/25.0
                changed = True
            if self.state == "strike" and now >= self.next_impact:
                # Schedule the next beat from its deadline, not from render time.
                missed = int((now-self.next_impact)/self.strike_beat)+1
                landed = min(missed,(self.door_hp+SHOOTING_MONSTER_DAMAGE-1)//SHOOTING_MONSTER_DAMAGE)
                self.last_impact_hand = ("left","right")[(self.strike_impact_index+landed-1)%2]
                self.strike_impact_index += landed
                self.next_impact += missed*self.strike_beat
                self.impacts += landed
                self.door_hp = max(0,self.door_hp-landed*SHOOTING_MONSTER_DAMAGE)
                if self.door_hp == 0:
                    self.breach_geometry = self.geometry(now)
                    self.state = "breached"
                    self.next_impact = float("inf")
                self.impact_until = now+.16
                renpy.music.play("audio/Audio/door .wav",channel="shooting_test_monster",loop=False)
                changed = True
            if self.auto_respawn and self.state == "gone" and now >= self.respawn_at:
                self.restart(delay=.8)
                changed = True
            renpy.redraw(self,0)
            return changed

        def hit_bounds(self,now):
            if self.state not in ("approach","windup","strike"):
                return None
            x,foot,size = self.geometry(now)
            return x-.26*size,foot-.97*size,.52*size,.75*size

        def clip_hit_bounds(self,bounds):
            if bounds is None:
                return ()
            left,top,width,height = bounds
            rectangles = []
            for x,y,w,h in SHOOTING_MONSTER_PANES:
                x1,y1 = max(left,x),max(top,y)
                x2,y2 = min(left+width,x+w),min(top+height,y+h)
                if x2 > x1 and y2 > y1:
                    rectangles.append((x1,y1,x2-x1,y2-y1))
            return tuple(rectangles)

        def hit_rectangles(self,now):
            return self.clip_hit_bounds(self.hit_bounds(now))

        def head_rectangles(self,now):
            if self.hit_bounds(now) is None:
                return ()
            x,foot,size = self.geometry(now)
            return self.clip_hit_bounds((x-.12*size,foot-.97*size,.24*size,.22*size))

        def hit_zone(self,aim,now):
            if not self.hit_test(aim,now):
                return None
            if any(x <= aim[0] < x+w and y <= aim[1] < y+h
                for x,y,w,h in self.head_rectangles(now)):
                return "head"
            return "body"

        def hit_test(self,aim,now):
            return any(x <= aim[0] < x+w and y <= aim[1] < y+h
                    for x,y,w,h in self.hit_rectangles(now))

        def debug_render(self,now):
            bounds = self.hit_bounds(now)
            if bounds is None:
                return None
            x,y,w,h = bounds
            result = renpy.Render(int(math.ceil(w))+8,int(math.ceil(h))+8)
            canvas = result.canvas()
            canvas.rect((255,80,80,255),(3,3,int(w),int(h)),1)
            for rx,ry,rw,rh in self.hit_rectangles(now):
                rect = (int(rx-x)+3,int(ry-y)+3,max(1,int(rw)),max(1,int(rh)))
                canvas.rect((255,215,60,48),rect)
                canvas.rect((255,215,60,255),rect,2)
            for rx,ry,rw,rh in self.head_rectangles(now):
                rect = (int(rx-x)+3,int(ry-y)+3,max(1,int(rw)),max(1,int(rh)))
                canvas.rect((255,125,230,65),rect)
                canvas.rect((255,125,230,255),rect,2)
            return result,(x-3,y-3)

        def take_hit(self,now,point=None):
            x,foot,size = self.geometry(now)
            px,py = point if point is not None else (x,foot-.65*size)
            zone = self.hit_zone((px,py),now)
            if zone is None:
                return None
            self.last_hit_zone = zone
            damage = SHOOTING_MONSTER_HEAD_DAMAGE if zone == "head" else SHOOTING_MONSTER_BODY_DAMAGE
            self.hp = max(0,self.hp-damage)
            self.hit_until = now+.32
            self.blood_events.append((now,px,py,self.blood_size(size)))
            self.blood_events = self.blood_events[-4:]
            if self.hp <= 0:
                self.state = "gone"
                self.kills += 1
                self.respawn_at = now+2.9
                self.next_impact = float("inf")
                self.impact_until = 0
                renpy.music.stop(channel="shooting_test_monster")
            # Nonfatal hits never reset progress, gait, windup or strike clocks.
            renpy.redraw(self,0)
            return zone

        def render(self,width,height,st,at):
            result = renpy.Render(1920,1080)
            if self.state != "waiting":
                # Place the feet explicitly in world pixels. The scaled image
                # is rendered inside a fresh small Render, avoiding nested
                # transform anchor inheritance from its cached source poses.
                now = math.floor(time.perf_counter()*25)/25.0
                x,foot,size = self.geometry(now)
                pose_index = self.frame_at(now)
                source = self.lit_frames[pose_index]
                if self.state == "gone":
                    fade = max(0,min(8,int((now-(self.respawn_at-2.9))/.4*8)))
                    source = self.lit_death_frames[fade]
                image = renpy.render(source,720,720,st,at)
                # The claw atlas reserves 11% above the crown for raised hands.
                # Keep crown/feet at the same world positions as the run poses.
                draw_size = size/.89 if pose_index >= 8 or self.state == "gone" else size
                scaled = renpy.Render(int(math.ceil(draw_size)),int(math.ceil(draw_size)))
                scaled.blit(image,(0,0))
                scaled.zoom(draw_size/720.0,draw_size/720.0)
                result.blit(scaled,(x-draw_size/2,foot-draw_size))
                for started,px,py,effect_size in self.blood_events:
                    age = max(0,now-started)
                    if age >= SHOOTING_MONSTER_BLOOD_DURATION:
                        continue
                    frame = min(7,int(age*25))
                    particle = renpy.render(SHOOTING_MONSTER_BLOOD_FRAMES[frame],160,160,st,at)
                    puff = renpy.Render(int(math.ceil(effect_size)),int(math.ceil(effect_size)))
                    puff.blit(particle,(0,0))
                    puff.zoom(effect_size/160.0,effect_size/160.0)
                    result.blit(puff,(px-effect_size/2,py-effect_size/2))
            renpy.redraw(self,.04)
            return result
