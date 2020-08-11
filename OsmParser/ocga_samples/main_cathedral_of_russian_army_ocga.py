"""
OCGA/PY rules example
Main Cathedral of the Russian Armed Forces
(c) Zkir 2020
"""
#from zcga import ZCGAContext as ctx


def checkRulesMy(ctx):
    if ctx.getTag("building") != "":

        # align local coordinates so that X matches the longest dimension, and oriented east
        ctx.rotateScope(10.52)

        ctx.setTag("building:colour","#103010")
        ctx.setTag("building:material","plaster")

        # we will start from the rectangle and will rebuild the form
        # basing of this very algorithm
        ctx.outerRectangle("mass_model")

    if ctx.getTag("building:part") == "mass_model":
        ctx.split_x((("~1","belltower_block"),(ctx.scope_sy()+5, "main_block_pre")))

    if ctx.getTag("building:part") == "belltower_block":
        ctx.scale("'1",ctx.scope_sx(),70)
        ctx.setTag("roof:shape", "onion")
        ctx.setTag("roof:height", "12")
        ctx.setTag("roof:colour", "gold")
        ctx.setTag("roof:material", "metal")
        ctx.split_z_preserve_roof((("~1.4", "belltower_layer1"),("~0.4", "belltower_layer1a"),
                                   ("~1.4", "belltower_layer2_pre"),
                                   ("~0.5", "belltower_layer3_pre")))

    if ctx.getTag("building:part") == "belltower_layer1":
        pass

    if ctx.getTag("building:part") == "belltower_layer1a":
        ctx.bevel(2)

    if ctx.getTag("building:part") == "belltower_layer2_pre":
        ctx.scale("'0.8","'0.8")
        ctx.split_x((("~1","belltower_layer2_portico_pre"),("~6","belltower_layer2_x"),("~1","belltower_layer2_portico_pre")))

    if ctx.getTag("building:part") == "belltower_layer2_x":
        ctx.split_y((("~1","belltower_layer2_portico"),("~6","belltower_layer2"),("~1","belltower_layer2_portico")))

    if ctx.getTag("building:part") == "belltower_layer2":
        ctx.bevel(2.5)

    if ctx.getTag("building:part") == "belltower_layer2_portico_pre":
        ctx.split_y(
            (("~1", "NIL"), ("~6", "belltower_layer2_portico"), ("~1", "NIL")))

    if ctx.getTag("building:part") == "belltower_layer2_portico":
        ctx.alignXToLongerScopeSide()
        ctx.scale(ctx.scope_sx()-2, "'1.2","'0.8")
        ctx.setTag("roof:shape","gabled")
        ctx.setTag("roof:height", "2")
        ctx.setTag("roof:orientation", "across")

    if ctx.getTag("building:part") == "belltower_layer3_pre":
        ctx.scale("'0.5", "'0.5")
        ctx.primitiveCylinder()
        ctx.setTag("roof:shape", "dome")  # onion
        ctx.setTag("roof:height", ctx.scope_sx() / 2)
        ctx.comp_roof("belltower_layer3a")
        ctx.setTag("building:part", "helm1")

    if ctx.getTag("building:part") == "belltower_layer3a":
        ctx.translate(0, 0, ctx.scope_sx() / 3.5)
        ctx.scale("'0.8", "'0.8", "'1")
        ctx.setTag("roof:shape", "pyramidal")  # onion
        ctx.setTag("building:part", "helm2")

    if ctx.getTag("building:part") == "main_block_pre":
        ctx.split_x((("~1","west_apse_block"), ("~4", "main_block"), ("~1","apse_block")))

    if ctx.getTag("building:part") == "apse_block":
        ctx.scale("'1", "'0.4")
        if ctx.current_object.relative_Ox < 0:
            ctx.rotateScope(180)
        ctx.split_z_preserve_roof((("~1", "apse_1_pre"), ("~1.25", "apse_2_pre"),("~2.75", "NIL")))

    if ctx.getTag("building:part") == "apse_1_pre":
        ctx.scale("'1", "'1", ctx.scope_sz() + 5)
        ctx.setTag("roof:shape", "half-dome")
        ctx.setTag("roof:height", "5")
        ctx.setTag("roof:material", "glass")
        ctx.setTag("roof:colour", "gray")
        ctx.primitiveHalfCylinder()

    if ctx.getTag("building:part") == "apse_2_pre":
        ctx.translate("-4.30",0)
        ctx.scale("'0.9","'0.605")
        ctx.setTag("roof:shape", "half-dome")
        ctx.setTag("roof:height", "6")
        ctx.setTag("roof:colour", "gold")
        ctx.setTag("roof:material", "metal")
        ctx.primitiveHalfCylinder()

    if ctx.getTag("building:part") == "west_apse_block":
        ctx.scale("'1", "'0.4")
        if ctx.current_object.relative_Ox < 0:
            ctx.rotateScope(180)
        ctx.split_z_preserve_roof((("~1", "west_apse_1_pre"), ("~1.25", "apse_2_pre"),("~2.75", "NIL")))

    if ctx.getTag("building:part") == "west_apse_1_pre":
        ctx.scale("'1", "'1", ctx.scope_sz() + 5)
        ctx.setTag("roof:shape", "half-dome")
        ctx.setTag("roof:height", "5")
        ctx.setTag("roof:material", "glass")
        ctx.setTag("roof:colour", "gray")
        ctx.bevel(6,[0,3])

    if ctx.getTag("building:part") == "main_block":
        ctx.split_y((("~0.4", "NIL"),("~0.6", "entrance"), ("~4", "cube"), ("~0.6", "entrance"),("~0.4", "NIL")))

    if ctx.getTag("building:part") == "entrance":
        ctx.scale("'0.3","'1","18")
        ctx.setTag("roof:shape", "round")
        if ctx.scope_sx() > ctx.scope_sy():
            ctx.setTag("roof:orientation", "across")
        else:
            ctx.setTag("roof:orientation", "along")

        ctx.setTag("roof:height", "6")

    if ctx.getTag("building:part") == "cube":
        ctx.split_z_preserve_roof((("~1", "cube1"), ("~4", "cube2")))

    if ctx.getTag("building:part") == "cube1":
        ctx.scale("'1", "'1", ctx.scope_sz() + 5)
        ctx.bevel(6)
        ctx.setTag("roof:shape","dome")
        ctx.setTag("roof:height", "5")
        ctx.setTag("roof:material", "glass")
        ctx.setTag("roof:colour", "gray")


    if ctx.getTag("building:part") == "cube2":
        ctx.scale("'0.8", "'0.8")
        ctx.split_x((("~1", "sideL"), ("~1.73", "cube3"), ("~1", "sideR")))


    if ctx.getTag("building:part") == "sideL":
        ctx.split_y((("~1", "side_head_L1"), ("~1.73", "side_erkerL"), ("~1", "side_head_L2")))

    if ctx.getTag("building:part") == "sideR":
        ctx.split_y((("~1", "side_head_R2"), ("~1.73", "side_erkerR"), ("~1", "side_head_R1")))

    if ctx.getTag("building:part") == "cube3":
        ctx.split_y((("~1", "side_erkerF"), ("~1.73", "main_head"), ("~1", "side_erkerB")))

    if ctx.getTag("building:part") == "main_head":
        ctx.setTag("roof:shape", "onion") # onion
        ctx.setTag("roof:height", "12")
        ctx.setTag("roof:colour", "gold")
        ctx.setTag("roof:material", "metal")
        ctx.split_z_preserve_roof(
            (("29", "main_head_layer1"), ("~1", "main_head_layer2_pre"), (1, "side_head_onion_base_pre")))

    if ctx.getTag("building:part") == "main_head_layer2_pre":
        ctx.scale("'0.8", "'0.8")
        ctx.rotateScope(22.5)
        ctx.primitiveCylinder(8)

    if ctx.getTag("building:part") == "side_head_L1":
        ctx.split_x((("~1","side_head"),))

    if ctx.getTag("building:part") == "side_head_L2":
        ctx.rotateScope(-90)
        ctx.split_x((("~1", "side_head"),))

    if ctx.getTag("building:part") == "side_head_R1":
        ctx.rotateScope(180)
        ctx.split_x((("~1", "side_head"),))

    if ctx.getTag("building:part") == "side_head_R2":
        ctx.rotateScope(-270)
        ctx.split_x((("~1", "side_head"),))

    if ctx.getTag("building:part") == "side_head":
        ctx.scale("'1","'1", "'0.75")
        ctx.setTag("roof:shape","onion") # onion
        ctx.setTag("roof:colour", "gold")
        ctx.setTag("roof:material", "metal")
        ctx.setTag("roof:height", "6")

        ctx.split_z_preserve_roof((("22","side_head_layer1"),("~1","side_head_layer2"),(1,"side_head_onion_base_pre")))

    if ctx.getTag("building:part") == "side_head_layer1":

        ctx.bevel(2.5, [0])

    if ctx.getTag("building:part") == "side_head_layer2":
        ctx.scale("'0.8", "'0.8")
        ctx.bevel(1.5)

    if ctx.getTag("building:part") == "side_head_onion_base_pre":
        ctx.primitiveCylinder()
        ctx.scale("'0.8", "'0.8")
        ctx.setTag("roof:shape", "dome")  # onion
        ctx.setTag("roof:height", ctx.scope_sx()/2)
        ctx.comp_roof("side_head_onion_base2")
        ctx.setTag("building:part", "helm1")

    if ctx.getTag("building:part") == "side_head_onion_base2":
        ctx.translate(0, 0, ctx.scope_sx() / 3.5)
        ctx.scale("'0.8", "'0.8","'1")
        ctx.setTag("roof:shape", "pyramidal")  # onion
        ctx.setTag("building:part", "helm2")


    if ctx.getTag("building:part") == "side_erkerL":
        ctx.rotateScope(0)
        ctx.split_x((("~1","side_erker"),))
    if ctx.getTag("building:part") == "side_erkerR":
        ctx.rotateScope(180)
        ctx.split_x((("~1", "side_erker"),))
    if ctx.getTag("building:part") == "side_erkerF":
        ctx.rotateScope(90)
        ctx.split_x((("~1", "side_erker"),))
    if ctx.getTag("building:part") == "side_erkerB":
        ctx.rotateScope(-90)
        ctx.split_x((("~1", "side_erker"),))

    if ctx.getTag("building:part") == ("side_erker"):
        ctx.scale("'1","'1", "'0.4")
        ctx.setTag("roof:shape", "gabled")
        ctx.setTag("roof:height", "5")
        ctx.setTag("roof:orientation", "across")

        ctx.scale(ctx.scope_sx()+6.10, "'1")
        ctx.translate(-6.10/2, 0)
        ctx.bevel(3.5, [0,3])
        ctx.comp_roof("side_erker_dome")

    if ctx.getTag("building:part") == ("side_erker_dome"):
        ctx.setTag("roof:shape", "half-dome")
        ctx.scale("'0.9", "'0.9", "7")
        ctx.setTag("roof:height", "7")

    if ctx.getTag("building:part") == "NIL":
        ctx.nil()

