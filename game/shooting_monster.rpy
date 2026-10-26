init python:
    import math
    import time

    SHOOTING_MONSTER_FRAMES = [
        Transform("images/shooting_test/monster/monster-%02d.png" % index, xysize=(720,720))
        for index in range(12)
    ]
    # Trapezoid traced from the user's marked street area in logical pixels.
    # The near sprite's head is y=316 (604px feet minus 288px height).
    SHOOTING_MONSTER_ROAD = ((855,520),(1060,520),(1510,604),(600,604))
    SHOOTING_MONSTER_LANES_FAR = (885,960,1035)
    SHOOTING_MONSTER_LANES_NEAR = (610,970,1420)
    SHOOTING_MONSTER_ROUTE_NAMES = ("Зүүн", "Гол", "Баруун")
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
            self.routes = [tuple(monster.geometry_at_progress(index/60.0,route)[:2]
                                for index in range(61)) for route in range(3)]

        def render(self,width,height,st,at):
            result = renpy.Render(1920,1080)
            canvas = result.canvas()
            points = SHOOTING_MONSTER_ROAD
            for first,second in zip(points,points[1:]+points[:1]):
                canvas.line((50,240,110,255),first,second,3)
            for route in self.routes:
                for first,second in zip(route,route[1:]):
                    canvas.line((70,185,255,230),first,second,2)
                canvas.circle((70,185,255,255),route[-1],5)
            return result

    class ShelterDoorMonster(renpy.Displayable):
        approach_duration = 4.0
        strike_duration = .96

        def __init__(self,**kwargs):
            super(ShelterDoorMonster,self).__init__(**kwargs)
            self.kills = 0
            self.impacts = 0
            self.route_index = -1
            self.death_frames = [Transform(SHOOTING_MONSTER_FRAMES[8],alpha=(8-index)/8.0)
                                for index in range(9)]
            self.restart(delay=1.2)

        def restart(self,delay=0,route=None):
            now = time.perf_counter()
            self.route_index = (self.route_index+1)%3 if route is None else int(route)%3
            self.state = "waiting"
            self.approach_started = now+delay
            self.strike_started = 0
            self.next_impact = float("inf")
            self.impact_until = 0
            self.hit_until = 0
            self.respawn_at = 0
            self.hp = 3
            renpy.music.stop(channel="shooting_test_monster")
            renpy.redraw(self,0)

        def visit(self):
            return SHOOTING_MONSTER_FRAMES+self.death_frames

        def geometry(self,now):
            progress = max(0,min(1,(now-self.approach_started)/self.approach_duration))
            return self.geometry_at_progress(progress)

        def geometry_at_progress(self,progress,route=None):
            progress = max(0,min(1,progress))
            route = self.route_index if route is None else int(route)%3
            depth = progress**1.25
            # Alternate the starting lane and smoothly cross toward the selected
            # near lane. No random waypoint jump or lateral teleport at a turn.
            start_route = (1,0,1)[route]
            lane_change = min(1,progress/.85)
            lane_change = lane_change*lane_change*(3-2*lane_change)
            far = SHOOTING_MONSTER_LANES_FAR
            near = SHOOTING_MONSTER_LANES_NEAR
            start_x = far[start_route]+(near[start_route]-far[start_route])*depth
            end_x = far[route]+(near[route]-far[route])*depth
            x = start_x+(end_x-start_x)*lane_change
            return x,520+84*depth,72+216*depth

        def frame_at(self,now):
            if self.state == "strike":
                phase = (now-self.strike_started) % self.strike_duration
                return 8+(0 if phase < .24 else (1 if phase < .48 else (2 if phase < .64 else 3)))
            return int(max(0,now-self.approach_started)*12.5) % 8

        def advance(self,now):
            changed = False
            if self.state == "waiting" and now >= self.approach_started:
                self.state = "approach"
                changed = True
            if self.state == "approach" and now >= self.approach_started+self.approach_duration:
                self.state = "strike"
                self.strike_started = now
                self.next_impact = now+.48
                changed = True
            if self.state == "strike" and now >= self.next_impact:
                # Schedule the next beat from its deadline, not from render time.
                missed = int((now-self.next_impact)/self.strike_duration)+1
                self.next_impact += missed*self.strike_duration
                self.impacts += 1
                self.impact_until = now+.16
                renpy.music.play("audio/Audio/door .wav",channel="shooting_test_monster",loop=False)
                changed = True
            if self.state == "gone" and now >= self.respawn_at:
                self.restart(delay=.8)
                changed = True
            renpy.redraw(self,0)
            return changed

        def hit_bounds(self,now):
            if self.state not in ("approach","strike"):
                return None
            x,foot,size = self.geometry(now)
            return x-.26*size,foot-.97*size,.52*size,.75*size

        def hit_rectangles(self,now):
            bounds = self.hit_bounds(now)
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
            return result,(x-3,y-3)

        def take_hit(self,now):
            self.hp -= 1
            self.hit_until = now+.32
            if self.hp <= 0:
                self.state = "gone"
                self.kills += 1
                self.respawn_at = now+2.9
                self.next_impact = float("inf")
                self.impact_until = 0
                renpy.music.stop(channel="shooting_test_monster")
            elif self.state == "approach":
                self.approach_started += .25
            elif self.state == "strike":
                self.strike_started = now
                self.next_impact = now+.8
            renpy.redraw(self,0)

        def render(self,width,height,st,at):
            result = renpy.Render(1920,1080)
            if self.state != "waiting":
                # Place the feet explicitly in world pixels. The scaled image
                # is rendered inside a fresh small Render, avoiding nested
                # transform anchor inheritance from its cached source poses.
                now = math.floor(time.perf_counter()*25)/25.0
                x,foot,size = self.geometry(now)
                size *= 1-.035*max(0,min(1,(self.hit_until-now)/.32))
                source = SHOOTING_MONSTER_FRAMES[self.frame_at(now)]
                if self.state == "gone":
                    fade = max(0,min(8,int((now-(self.respawn_at-2.9))/.4*8)))
                    source = self.death_frames[fade]
                image = renpy.render(source,720,720,st,at)
                scaled = renpy.Render(int(math.ceil(size)),int(math.ceil(size)))
                scaled.blit(image,(0,0))
                scaled.zoom(size/720.0,size/720.0)
                result.blit(scaled,(x-size/2,foot-size))
            renpy.redraw(self,.04)
            return result
