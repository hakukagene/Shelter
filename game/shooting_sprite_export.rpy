# Development-only asset bake. Excluded from distributions with its .rpyc.
init python:
    def shelter_export_shooting_sprites():
        import os
        root = os.path.join(config.basedir, "tools", "art", "shooting-test")
        output = os.path.join(config.gamedir, "images", "shooting_test", "sequence")
        os.makedirs(output, exist_ok=True)

        def load_source(relative):
            with open(os.path.join(root, relative), "rb") as source:
                return im.Data(source.read(), relative)

        names = ("idle", "fire", "settle", "reload-start", "reload-out", "reload-in", "reload-rack", "reload-ready")
        sleeve = Transform(load_source("sleeve-extension.png"), xysize=(650,1100))
        poses = []
        for index, name in enumerate(names):
            image = Transform(load_source("source-poses/"+name+".png"), xysize=(800,800))
            layers = [(-250,140), sleeve] if index == 6 else []
            layers += [(200,0), image]
            poses.append(Composite((1200,1000), *layers))

        # Source poses remain archival artwork; all runtime animation is baked.
        keys = ((0,0,0),(.05,0,-1),(.11,3,-3),(.18,3,-5),(.25,4,-6),(.32,4,-7),
                (.39,4,-6),(.46,5,-5),(.53,5,-3),(.60,5,-1),(.67,6,1),(.74,6,3),
                (.81,6,1),(.88,7,-1),(.94,7,-.5),(1,0,0))
        boundaries = ((.11,0,3),(.25,3,4),(.46,4,5),(.67,5,6),(.88,6,7),(1,7,0))

        def tilt(phase):
            for first, second in zip(keys, keys[1:]):
                if phase < second[0]:
                    ratio = (phase-first[0])/(second[0]-first[0])
                    ratio = ratio*ratio*(3-2*ratio)
                    return first[2]+(second[2]-first[2])*ratio
            return 0

        def save(name, pose, angle=0, blend_time=0):
            posed = Transform(pose, rotate=angle, xpos=600, ypos=656,
                              xanchor=.5, yanchor=.656, transform_anchor=True)
            stage = Fixed(posed, xysize=(1200,1000))
            # Half resolution keeps all 56 decoded sprites around 64 MB.
            displayable = Transform(stage, xysize=(600,500))
            renpy.render_to_file(displayable, os.path.join(output,name),
                                 width=600,height=500,st=blend_time,resize=True)

        renpy.start_predict(*poses)
        save("idle.png",poses[0])
        for index in range(10):
            elapsed = index/25.0
            frame = 1 if elapsed < .065 else (2 if elapsed < .18 else 0)
            recoil = 2*math.sin(math.pi*min(1,elapsed/.24))
            save("fire-%02d.png" % index,poses[frame],recoil)
        for index in range(45):
            phase = index/44.0
            current = poses[0]
            blend = 0
            for boundary, previous, following in boundaries:
                half_width = .04/1.8
                if phase < boundary-half_width:
                    current = poses[previous]
                    break
                if phase <= boundary+half_width:
                    blend = max(0,min(1,(phase-boundary+half_width)/(2*half_width)))
                    blend = blend*blend*(3-2*blend)
                    current = renpy.display.transition.Dissolve(1,old_widget=poses[previous],new_widget=poses[following],alpha=True)
                    break
                current = poses[following]
            # Exact endpoint avoids a partial final dissolve snapping to idle.
            if index == 44:
                current, blend = poses[0], 0
            save("reload-%02d.png" % index,current,tilt(phase),blend)
        renpy.stop_predict(*poses)
        print("Exported 56 transparent sprites: idle + 10 fire + 45 reload frames.")

testsuite shelter_sprite_export:
    teardown:
        exit
    testcase bake:
        pause until screen "main_menu" timeout 10
        run Function(shelter_export_shooting_sprites)
        exit
