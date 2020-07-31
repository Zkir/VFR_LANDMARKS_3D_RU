"""
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

        #ctx.nil()

    if ctx.getTag("building:part") == "mass_model":
        ctx.split_x((("~1","belltower_block"),(ctx.scope_sy()+5, "main_block_pre")))

    if ctx.getTag("building:part") == "belltower_block":
        ctx.scale("'1",ctx.scope_sx(),70)
        ctx.setTag("roof:shape", "onion")
        ctx.setTag("roof:height", "12")
        ctx.setTag("roof:colour", "gold")
        ctx.setTag("roof:material", "metal")
        ctx.split_z_preserve_roof((("~1.5", "belltower_layer1"), ("~1.25", "belltower_layer2_pre"), ("~0.7", "belltower_layer3_pre")))

    if ctx.getTag("building:part") == "belltower_layer1":
        pass

    if ctx.getTag("building:part") == "belltower_layer2_pre":
        ctx.scale("'0.8","'0.8")
        ctx.split_x((("~1","belltower_layer2_portico_pre"),("~6","belltower_layer2_x"),("~1","belltower_layer2_portico_pre")))

    if ctx.getTag("building:part") == "belltower_layer2_x":
        ctx.split_y((("~1","belltower_layer2_portico"),("~6","belltower_layer2"),("~1","belltower_layer2_portico")))

    if ctx.getTag("building:part") == "belltower_layer2":
        ctx.bevel(2)

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
        ctx.primitiveCircle("belltower_layer3")

    if ctx.getTag("building:part") == "main_block_pre":
        ctx.split_x((("~1","apse_block"), ("~4", "main_block"), ("~1","apse_block")))

    if ctx.getTag("building:part") == "apse_block":
        ctx.scale("'1", "'0.3")
        if ctx.current_object.relative_Ox < 0:
            ctx.rotateScope(180)
        ctx.split_z_preserve_roof((("~1", "apse_1_pre"), ("~1", "apse_2_pre"),("~2", "NIL")))

    if ctx.getTag("building:part") == "apse_1_pre":
        ctx.scale("'1", "'1", ctx.scope_sz() + 5)
        ctx.setTag("roof:shape", "half-dome")
        ctx.setTag("roof:height", "5")
        ctx.setTag("roof:material", "glass")
        ctx.setTag("roof:colour", "gray")
        ctx.primitiveHalfCircle("apse")

    if ctx.getTag("building:part") == "apse_2_pre":
        ctx.translate("'-0.2",0)
        ctx.scale("'0.6","'0.6")
        ctx.setTag("roof:shape", "half-dome")
        ctx.setTag("roof:height", "6")
        ctx.setTag("roof:colour", "gold")
        ctx.setTag("roof:material", "metal")
        ctx.primitiveHalfCircle("apse")




    if ctx.getTag("building:part") == "main_block":
        ctx.split_y((("~1", "entrance"), ("~4", "cube"), ("~1", "entrance")))

    if ctx.getTag("building:part") == "entrance":
        ctx.scale("'0.3","'1","18")
        ctx.setTag("roof:shape", "round")
        if ctx.scope_sx() > ctx.scope_sy():
            ctx.setTag("roof:orientation", "across")
        else:
            ctx.setTag("roof:orientation", "along")

        ctx.setTag("roof:height", "6")

    if ctx.getTag("building:part") == "cube":
        ctx.split_z_preserve_roof((("~1", "cube1"), ("~3", "cube2")))

    if ctx.getTag("building:part") == "cube1":
        ctx.scale("'1", "'1", ctx.scope_sz() + 5)
        ctx.bevel(6)
        ctx.setTag("roof:shape","dome")
        ctx.setTag("roof:height", "5")
        ctx.setTag("roof:material", "glass")
        ctx.setTag("roof:colour", "gray")


    if ctx.getTag("building:part") == "cube2":
        ctx.scale("'0.8", "'0.8")

    if ctx.getTag("building:part") == "cube2":
        ctx.split_x((("~1", "sideL"), ("~2.5", "cube3"), ("~1", "sideR")))


    if ctx.getTag("building:part") == "sideL":
        ctx.split_y((("~1", "side_head"), ("~2.5", "side_erkerL"), ("~1", "side_head")))

    if ctx.getTag("building:part") == "sideR":
        ctx.split_y((("~1", "side_head"), ("~2.5", "side_erkerR"), ("~1", "side_head")))

    if ctx.getTag("building:part") == "cube3":
        ctx.split_y((("~1", "side_erkerF"), ("~2.5", "main_head"), ("~1", "side_erkerB")))

    if ctx.getTag("building:part") == "main_head":
        ctx.setTag("roof:shape", "onion")
        ctx.setTag("roof:height", "20")
        ctx.setTag("roof:colour", "gold")
        ctx.setTag("roof:material", "metal")
        ctx.split_z_preserve_roof(
            (("22", "main_head_layer1"), ("~1", "main_head_layer2_pre"), (1, "side_head_onion_base_pre")))

    if ctx.getTag("building:part") == "main_head_layer2_pre":
        ctx.scale("'0.8", "'0.8")
        ctx.rotateScope(22.5)
        ctx.primitiveCircle("main_head_layer2",8)

    if ctx.getTag("building:part") == "side_head":
        ctx.scale("'1","'1", "'0.75")
        ctx.setTag("roof:shape","onion")
        ctx.setTag("roof:colour", "gold")
        ctx.setTag("roof:material", "metal")
        ctx.setTag("roof:height", "12")
        ctx.split_z_preserve_roof((("22","side_head_layer1"),("~1","side_head_layer2"),(1,"side_head_onion_base_pre")))

    if ctx.getTag("building:part") == "side_head_layer1":
        ctx.bevel(2.5, [0])

    if ctx.getTag("building:part") == "side_head_layer2":
        ctx.scale("'0.8", "'0.8")
        ctx.bevel(1.5)

    if ctx.getTag("building:part") == "side_head_onion_base_pre":
        ctx.scale("'0.775", "'0.775")
        ctx.primitiveCircle("side_head_onion_base")

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

    if ctx.getTag("building:part") in ("side_erker"):
        ctx.scale("'1","'1", "'0.4")
        ctx.setTag("roof:shape", "gabled")
        ctx.setTag("roof:height", "3")
        ctx.setTag("roof:orientation", "across")
        #dirty hack
        #ctx.translate(ctx.current_object.parent.parent.parent.scope_sx*0.3-ctx.scope_sx(), 0)
        ctx.scale(ctx.scope_sx()+6.10, "'1")
        ctx.translate(-6.10/2, 0)
        ctx.bevel(3.5,[0,3])

    if ctx.getTag("building:part") == "NIL":
        ctx.nil()

