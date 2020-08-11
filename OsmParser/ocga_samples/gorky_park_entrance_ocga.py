"""
Set of rules to generate some geometry for buildings,
first of all Gorky Park Entrance
(c) Zkir 2020
"""


def checkRulesMy(ctx):
    if ctx.getTag("building:part") == "porch":
        # align local coordinates so that X matches the longest dimension
        ctx.alignScopeToGeometry()
        ctx.alignXToLongerScopeSide()

        # we want to remove it, and replace with 3 orther objects: porch_base, porch_columns, porch_top
        # Split Z, preserve roof,  {1:porch_base| ~1:porch_columns | 1: porch_top}
        ctx.split_z_preserve_roof(("1", "porch_base"),
                                  ("~5", "porch_columns"),
                                  ("1", "porch_top"))

    elif ctx.getTag("building:part") == "porch_base":
        ctx.setTag("building:colour", "red")

    elif ctx.getTag("building:part") == "porch_columns":
        # split(x){ {~sy:porch_column_pre| ~sy:Nil}* | ~sy:porch_column_pre }
        ctx.split_x((("~1", "porch_column_pre"),
                     ("~1", "porch_column_pre"),
                     ("~1", "porch_column_pre"),
                     ("~1", "porch_column_pre")))

    elif ctx.getTag("building:part") == "porch_column_pre":
        ctx.split_z_preserve_roof((("~1", "porch_column_main"),
                                   ("0.25", "porch_column_top_pre")))

    elif ctx.getTag("building:part") == "porch_column_top_pre":
        top_size = min(ctx.scope_sx(), ctx.scope_sy()) / 1.0
        ctx.scale(top_size, top_size)
        ctx.setTag("building:part","porch_column_top")

    elif ctx.getTag("building:part") == "porch_column_main":
        # osmObject.osmtags["building:colour"] = "green"
        ctx.primitiveCylinder(12, min(ctx.scope_sx(), ctx.scope_sy()) / 3)

    elif ctx.getTag("building:part") == "porch_top":
        ctx.setTag("building:colour","blue")

    # ===========================================================================================================
    # Kokoshnik
    # ===========================================================================================================
    elif (ctx.getTag("building:part") != "") and (ctx.getTag("building:roof:kokoshniks") == "yes"):

        # what do we here?
        # some kind of the comp operator
        # for each edge of the tholobate we create kokoshnik.
        # remove the kokoshniks tag, to prevent dead loops.
        ctx.setTag("building:roof:kokoshniks", "")
        ctx.comp_border("kokoshnik_pre")
        ctx.restore()

    elif ctx.getTag("building:part") == "kokoshnik_pre":
        facade_len = ctx.scope_sx()
        ctx.setTag("building:part", "kokoshnik")
        ctx.setTag("roof:shape", "round")
        ctx.setTag("roof:orientation", "across")
        ctx.setTag("roof:height", str(facade_len / 2))
        ctx.setTag("height", str(ctx.getTag("min_height") + facade_len / 2 + 0.1))
        ctx.setTag("building:roof:kokoshniks", "")

    # ===========================================================================================================
    # Entrance to the Gorky Park
    # ===========================================================================================================
    elif ctx.getTag("building") == "triumphal_arch" and ctx.getTag(
            "building:architecture") == "stalinist_neoclassicism":

        if ctx.getTag("building:levels") != "" and ctx.getTag("height") == 0:
            ctx.setTag("height", str(float(ctx.getTag("building:levels")) * 4))

        ctx.setTag("building", "yes")

        # align local coordinates so that X matches the longest dimension
        ctx.alignScopeToGeometry()
        ctx.alignXToLongerScopeSide()
        ctx.split_x((("~1", "building_outline"),))
        ctx.restore()

    elif ctx.getTag("building:part") == "building_outline":
        # we need to do offset inside, to compensate cornice, which is huge
        ctx.scale(ctx.scope_sx() - 2.5, ctx.scope_sy() - 2.5)
        ctx.split_x((("~0.06", "side_column_block"),("~1", "pylon_pre"), ("~3.5", "arch"), ("~1", "pylon_pre"),("~0.06", "side_column_block")))

    elif ctx.getTag("building:part") == "arch":
        ctx.setTag("building:part", "no")
        ctx.scale(ctx.scope_sx(), ctx.scope_sy() - 2.0)
        ctx.split_z_preserve_roof((("0.2", "stilobate"),
                                   ("~4", "arch_columns"),
                                   ("~1.5", "pylon_middle"),  # arch_top_pre
                                   ("~1", "NIL")))


    elif ctx.getTag("building:part") == "pylon_pre":
        ctx.split_z_preserve_roof((("0.2", "stilobate"),
                                   ("~4", "pylon"),
                                   ("~1.5", "pylon_middle"),
                                   ("~1", "pylon_top")))

    elif ctx.getTag("building:part") == "side_column_block":
        ctx.rotateScope(90)
        ctx.split_x((("~1", "NIL"),("~1", "side_column_pre"), ("~1.5", "NIL"), ("~1", "side_column_pre"), ("~1", "NIL")))

    elif ctx.getTag("building:part") == "side_column_pre":
        ctx.split_z_preserve_roof((("0.2", "stilobate"),
                                   ("~4", "pylon"),
                                   ("~1.5", "pylon_middle"),
                                   ("~1", "NIL")))


    elif ctx.getTag("building:part") == "pylon_middle":
        ctx.split_z_preserve_roof( (("~1", "pylon_middle_wall"),
                                    ("0.6", "pylon_middle_cornice1_pre"),
                                    ("0.6", "pylon_middle_cornice2_pre"),
                                    ("~2", "pylon_middle_wall"),
                                    ("0.3", "pylon_middle_cornice3_pre"),
                                    ("0.3", "pylon_middle_cornice4_pre")
                                                        ))

    elif ctx.getTag("building:part") == "pylon_middle_cornice1_pre":
        ctx.scale(ctx.scope_sx() + 1.4, ctx.scope_sy() + 1.4)
        ctx.setTag("building:part", "cornice1")

    elif ctx.getTag("building:part") == "pylon_middle_cornice2_pre":
        ctx.scale(ctx.scope_sx() + 2.45, ctx.scope_sy() + 2.45)
        ctx.setTag("building:part", "cornice2")

    elif ctx.getTag("building:part") == "pylon_middle_cornice3_pre":
        ctx.scale(ctx.scope_sx() + 0.4, ctx.scope_sy() + 0.4)
        ctx.setTag("building:part", "cornice3")

    elif ctx.getTag("building:part") == "pylon_middle_cornice4_pre":
        ctx.scale(ctx.scope_sx() + 0.9, ctx.scope_sy() + 0.9)
        ctx.setTag("building:part", "cornice4")

    elif ctx.getTag("building:part") == "pylon_top":
        ctx.split_z_preserve_roof((("~1", "pylon_top1_pre"),
                                   ("~1", "pylon_top2_pre"),
                                   ("~1", "pylon_top3_pre")))

    elif ctx.getTag("building:part") == "pylon_top1_pre":
        ctx.split_x((("1.0", "pylon_top1_obelisk_block"),
                    ("~1", "pylon_top1_pre2"),
                    ("1.0", "pylon_top1_obelisk_block")))

    elif ctx.getTag("building:part") == "pylon_top1_pre2":
        ctx.scale((ctx.scope_sx()+2*1.0) * 0.6, ctx.scope_sy() * 0.6)
        ctx.setTag("building:part",  "pylon_top1")

    elif ctx.getTag("building:part") == "pylon_top1_obelisk_block":
        ctx.rotateScope(90)
        ctx.split_x((("1", "pylon_top1_obelisk_pre"),
                    ("~10", "NIL"),
                    ("1", "pylon_top1_obelisk_pre")))

    elif ctx.getTag("building:part") == "pylon_top1_obelisk_pre":
        #ctx.scale("'1", "'1", 1.8 )
        ctx.scale(ctx.scope_sx(), ctx.scope_sy(), 1.8)
        ctx.setTag("building:part", "obelisk")
        ctx.setTag("roof:shape", "skillion")
        ctx.setTag("roof:height", "1.75")
        ctx.setTag("roof:direction", str(90+ctx.scope_rz()))

    elif ctx.getTag("building:part") == "pylon_top2_pre":
        ctx.scale(ctx.scope_sx() * 0.5, ctx.scope_sy() * 0.5)
        ctx.setTag("building:part", "pylon_top2")

    elif ctx.getTag("building:part") == "pylon_top3_pre":
        ctx.scale(ctx.scope_sx() * 0.4, ctx.scope_sy() * 0.4)
        ctx.setTag("building:part", "pylon_top3")

    elif ctx.getTag("building:part") == "arch_columns":
        #ctx.setTag("building:part","no")

        ctx.split_x((("~0.2", "semi_column_block"), ("~1.2", "NIL"),
                                                    ("~1", "arch_column_block"), ("~1.1", "NIL"),
                                                    ("~1", "arch_column_block"), ("~1.1", "NIL"),
                                                    ("~1", "arch_column_block"), ("~1.1", "NIL"),
                                                    ("~1", "arch_column_block"), ("~1.1", "NIL"),
                                                    ("~1", "arch_column_block"), ("~1.1", "NIL"),
                                                    ("~1", "arch_column_block"), ("~1.2", "NIL"),
                                                    ("~0.2", "semi_column_block")))

    elif ctx.getTag("building:part") == "arch_column_block":
        ctx.setTag("building:part", "no")
        ctx.rotateScope(90)
        # split(x){ {~sy:porch_column_pre| ~sy:Nil}* | ~sy:porch_column_pre }
        ctx.split_x((("~1", "porch_column_pre"),
                     ("~0.2", "NIL"),
                     ("~1", "porch_column_pre"),
                     ("~1.1", "NIL"),
                     ("~1", "porch_column_pre"),
                     ("~0.2", "NIL"),
                     ("~1", "porch_column_pre")))

        # let's hope the grammar will allow such trick,
        # and the current shape is still the same, so we can split it twice
        ctx.split_x( (("~1", "obelisk_pre"),
                      ("~8", "NIL"),
                      ("~1", "obelisk_pre")))


    elif ctx.getTag("building:part") == "semi_column_block":
        ctx.setTag("building:part", "no")
        ctx.rotateScope(90)

        ctx.split_x( (("~1", "semi_column_pre"),
                      ("~0.2", "NIL"),
                      ("~1", "semi_column_pre"),
                      ("~1.1", "NIL"),
                      ("~1", "semi_column_pre"),
                      ("~0.2", "NIL"),
                      ("~1", "semi_column_pre")))

    elif ctx.getTag("building:part") == "semi_column_pre":
        ctx.split_z_preserve_roof((("~1", "semi_column_main"),
                                   ("0.25", "semi_column_top")))

    elif ctx.getTag("building:part") == "semi_column_top":
        ctx.setTag("building:part", "abacus")
        ctx.scale(ctx.scope_sx(), ctx.scope_sy() + 0.5)

    elif ctx.getTag("building:part") == "semi_column_main":
        ctx.setTag("building:part", "fustis")
        ctx.scale(ctx.scope_sx() - 0.5, ctx.scope_sy())

    elif ctx.getTag("building:part") == "obelisk_pre":
        ctx.setTag("building:part", "obelisk")
        ctx.scale(1, 1.5)
        ctx.setTag("building:part", "yes")
        ctx.setTag("min_height", "18.3")
        ctx.setTag("height", "20.1")
        ctx.setTag("roof:height", "1.70")
        ctx.setTag("roof:shape", "round")
        ctx.setTag("roof:orientation", "across")

    elif ctx.getTag("building:part") == "NIL":
        ctx.nil()