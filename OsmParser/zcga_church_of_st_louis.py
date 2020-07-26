"""
Set of rules to generate church of St Louis of France, Moscow
(c) Zkir 2020
"""


def checkRulesMy(ctx):
    if ctx.getTag("building") != "":

        # guess height
        if ctx.getTag("building:levels") != "" and ctx.getTag("height") == 0:
            ctx.setTag("height", str(float(ctx.getTag("building:levels")) * 4))

        # align local coordinates so that X matches the longest dimension
        ctx.alignScopeToGeometry()
        ctx.alignX2LongerScopeSide()
        ctx.rotateScope(180)
        ctx.split_x((("~1", "mass_model"),))
        ctx.restore()

    elif ctx.getTag("building:part") == "mass_model":
        ctx.scale("'0.9", "'0.95")
        ctx.split_x(((2.5, "parvise_block"),("~0.75", "entrance_block"), ("~5", "main_block"), ("~1", "apse_block")))

    elif ctx.getTag("building:part") == "parvise_block":
        ctx.scale("'1", "'0.9","1.5")
        ctx.split_y(((4, "parvise"), ("~5", "parvise_steps_pre"), (4, "parvise")))

    elif ctx.getTag("building:part") == "parvise_steps_pre":
        ctx.setTag("building:part", "steps")
        ctx.setTag("roof:shape","skillion")
        ctx.setTag("roof:height", ctx.getTag("height")-0.1)
        azimuth = (360 + 90 - ctx.scope_rz()) % 360  # from mathematical angle to geographical azimuth.
        # geographical azimuth is counted from north clockwise

        ctx.setTag("roof:direction", (360+180+azimuth)%360)

    elif ctx.getTag("building:part") == "entrance_block":
        ctx.scale("'1", "'0.9")
        ctx.split_y(((ctx.scope_sx(), "bell_tower"), ("~5", "portico"), (ctx.scope_sx(), "bell_tower")))

    #bell towers
    elif ctx.getTag("building:part") == "bell_tower":
        ctx.scale("'1","'1","11")
        ctx.split_z_preserve_roof((("7.0", "bell_tower_layer_1"), ("3.8", "bell_tower_layer_2"), ("~0.5", "bell_tower_dome_pre")))

    elif ctx.getTag("building:part") == "bell_tower_layer_1":
        pass

    elif ctx.getTag("building:part") == "bell_tower_layer_2":
        ctx.scale(ctx.scope_sx()-0.5, ctx.scope_sy()-0.5)
        ctx.setTag("roof:shape", "pyramidal")
        ctx.setTag("roof:height", "0.75")
        ctx.setTag("height", ctx.getTag("height")+0.75)

    elif ctx.getTag("building:part") == "bell_tower_dome_pre":
        ctx.scale(ctx.scope_sx() - 1, ctx.scope_sy() - 1,(ctx.scope_sy() - 1)/2*1.2)
        ctx.setTag("roof:shape", "dome")
        ctx.setTag("roof:height", ctx.scope_sy()/2 )
        ctx.primitiveCircle("bell_tower_dome")

    # portico
    elif ctx.getTag("building:part") == "portico":
        ctx.scale(ctx.scope_sx()+ 1,"'1", 7+1.5+0.2  )
        ctx.setTag("roof:shape", "gabled")
        ctx.setTag("roof:orientation", "across")
        ctx.setTag("roof:height", "1.5")
        ctx.split_z_preserve_roof((("1.5", "portico_stilobate"),
                                  ("~5", "portico_columns_block"),
                                  ("1.5", "portico_entablement"),
                                  ("0.2", "portico_top")))

    elif ctx.getTag("building:part") == "portico_stilobate":
        pass

    elif ctx.getTag("building:part") == "portico_columns_block":
        ctx.split_x((("~1", "portico_columns"), ("~2", "NIL")))

    elif ctx.getTag("building:part") == "portico_columns":
        ctx.split_y((("~1", "porch_column_pre"), ("~0.7", "NIL"),
                     ("~1", "porch_column_pre"), ("~0.7", "NIL"),
                     ("~1", "porch_column_pre"), ("~0.7", "NIL"),
                     ("~1", "porch_column_pre"),("~0.7", "NIL"),
                     ("~1", "porch_column_pre"),("~0.7", "NIL"),
                     ("~1", "porch_column_pre")))

    elif ctx.getTag("building:part") == "porch_column_pre":
        ctx.split_z_preserve_roof((("~1", "porch_column_main"),
                                   ("0.25", "porch_column_top_pre")))

    elif ctx.getTag("building:part") == "porch_column_top_pre":
        top_size = min(ctx.scope_sx(), ctx.scope_sy()) / 1.0
        ctx.scale(top_size, top_size)
        ctx.setTag("building:part", "porch_column_top")

    elif ctx.getTag("building:part") == "porch_column_main":
        # osmObject.osmtags["building:colour"] = "green"
        ctx.primitiveCircle("porch_column", 12, min(ctx.scope_sx(), ctx.scope_sy()) / 3)

    elif ctx.getTag("building:part") == "portico_top":
        ctx.scale (ctx.scope_sx()+1.0, ctx.scope_sy()+1.0)

    # main block
    elif ctx.getTag("building:part") == "main_block":
        ctx.split_y((("~1", "main_side_part_pre"),
                     ("~2", "main_main"),
                     ("~1", "main_side_part_pre")))

    elif ctx.getTag("building:part") == "main_main":
        ctx.scale("'1", "'1", "13")
        ctx.setTag("roof:shape", "hipped")
        ctx.setTag("roof:height", "1.5")

    elif ctx.getTag("building:part") == "main_side_part_pre":
        ctx.scale("'1","'1","8.5")
        ctx.setTag("roof:shape", "skillion")
        ctx.setTag("roof:height", "1.5")
        azimuth =(360+90-ctx.scope_rz())%360 # from mathematical angle to geographical azimuth.
                                             # geographical azimuth is counted from north clockwise

        if ctx.current_object.relative_Oy > 0:
            # "undocumented" experimenal function
            # skillion roof should have upper edge from "inside" and lower from "outside"
            # we try to define what is inside and what is outside by relative location of the split parts (relative to parent)
            azimuth = (360+azimuth-90) % 360
        else:
            azimuth = (360+azimuth+90) % 360
        ctx.setTag("roof:direction", azimuth)

    #apse block
    elif ctx.getTag("building:part") == "apse_block":
        ctx.split_y((("~1", "side_part_1_pre"),
                     ("1", "NIL"),
                     ("~2", "apse_pre"),
                     ("0.5", "NIL"),
                     ("~1", "side_part_2_pre")))

    elif ctx.getTag("building:part") == "apse_pre":
        ctx.setTag("height",10)
        ctx.setTag("roof:shape", "half-dome")
        ctx.setTag("roof:height", "3")
        ctx.primitiveHalfCircle("apse", 8 )


    elif ctx.getTag("building:part") == "side_part_1_pre":
        ctx.split_x((("~1.5", "side_apse"), ("~1", "NIL")))
    elif ctx.getTag("building:part") == "side_part_2_pre":
        ctx.split_x((("~3", "side_apse"), ("~1", "NIL")))

    elif ctx.getTag("building:part") == "side_apse":
        ctx.scale("'1","'1","6.5")
        ctx.setTag("roof:shape", "pyramidal")
        ctx.setTag("roof:height", "1")

    elif ctx.getTag("building:part") == "NIL":
        ctx.nil()
