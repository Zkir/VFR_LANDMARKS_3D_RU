"""
OCGA/PY rules example
Gorky Park Rotunda
(c) Zkir 2020
"""
HEIGHT_RATE=1.3
SNOP_HEIGHT=1.25

def checkRulesMy(ctx):
    if ctx.getTag("building") != "":
        if ctx.scope_sz() == 0:
            height = ctx.scope_sx()*HEIGHT_RATE+SNOP_HEIGHT
            ctx.setTag("height", height)
        ctx.massModel("mass_model")

    if ctx.getTag("building:part") == "mass_model":

        ctx.setTag("building:colour", "#B0B0B0")
        ctx.setTag("building:material", "plaster")

        ctx.split_z_preserve_roof((("0.6","stylobate"),
                                    ("~8.2", "collonade"),
                                    ("~1.5", "entablement"),
                                    ("~0.3", "cornice"),
                                    ("~6", "roof")))

    if ctx.getTag("building:part") == "stylobate":
        ctx.setTag("roof:colour", "#101010")
        ctx.setTag("roof:material", "stone")
        ctx.setTag("building:colour", "#202020")
        ctx.setTag("building:material", "stone")

        ctx.split_z_preserve_roof((("~1", "stylobate1"),
                                   ("~1", "stylobate2"),
                                   ("~1", "stylobate3")))

    if ctx.getTag("building:part") == "roof":
        ctx.scale("'0.9", "'0.9")
        ctx.setTag("roof:colour", "brown")
        ctx.setTag("roof:material", "metal")
        ctx.setTag("building:colour", "brown")
        ctx.setTag("building:material", "metal")
        ctx.split_z_preserve_roof((("~0.1", "roof1"),
                                   ("~3", "dome"),
                                   (SNOP_HEIGHT, "roof4")))

    if ctx.getTag("building:part") == "stylobate1":
        ctx.scale("'1.2", "'1.2")

    if ctx.getTag("building:part") == "stylobate2":
        ctx.scale("'1.1","'1.1")

    if ctx.getTag("building:part") == "stylobate3":
        ctx.scale("'1","'1")

    if ctx.getTag("building:part") == "collonade":
        ctx.scale("'0.9", "'0.9")
        ctx.comp_border(ctx.current_object.size/8, "column_pre")

    if ctx.getTag("building:part") == "entablement":
        ctx.scale("'0.9", "'0.9")

    if ctx.getTag("building:part") == "cornice":
        ctx.scale("'1","'1")

    if ctx.getTag("building:part") == "roof1":
        ctx.scale("'1","'1", 0.75)
        ctx.setTag("building:colour", "white")
        ctx.setTag("building:material", "plaster")
        #ctx.primitiveCylinder(32)
        ctx.comp_border(ctx.current_object.size/10, "roof_railing_pre")

    if ctx.getTag("building:part") == "roof_railing_pre":
        if ctx.current_object.split_index % 2 == 0:
            ctx.scale(ctx.scope_sy(), "'1")
            ctx.setTag("roof:shape", "pyramidal")
            ctx.setTag("roof:height", ctx.scope_sz()*0.2)
        else:
            ctx.scale("'1.5", "'0.3", "'0.75")
            ctx.split_z_preserve_roof((  ("~1","roof_railing_base"),("~5", "roof_railing_middle"),("~1","roof_railing_top")    ))

    if ctx.getTag("building:part") == "roof_railing_middle":
        #{{~scope_sy/2: nil| ~scope_sy:roof_column}* | ~scope_sy/2: nil  }
        ctx.split_x((("~0.5","nil"), ("~1","roof_column"),
                     ("~0.5","nil"), ("~1","roof_column"),
                     ("~0.5", "nil"), ("~1", "roof_column"),
                     ("~0.5", "nil"), ("~1", "roof_column"),
                     ("~0.5", "nil"), ("~1", "roof_column"),
                     ("~0.5", "nil"), ("~1", "roof_column"),
                     ("~0.5", "nil"), ("~1", "roof_column"),
                     ("~0.5", "nil"), ("~1", "roof_column"),
                     ("~0.5", "nil"), ("~1", "roof_column"),
                     ("~0.5","nil")))

    if ctx.getTag("building:part") == "roof_column":
        ctx.primitiveCylinder()

    if ctx.getTag("building:part") == "dome":
        ctx.scale("'0.85","'0.85")
        roof_height = ctx.getTag("height")-ctx.getTag("min_height")-0.01
        ctx.setTag("roof:shape", "dome")
        ctx.setTag("roof:height", roof_height)

    if ctx.getTag("building:part") == "roof4":
        ctx.scale("'0.1","'0.1")
        ctx.translate(0,0,"'-0.1")
        ctx.setTag("roof:colour", "gold")
        ctx.setTag("roof:material", "metal")
        ctx.setTag("building:colour", "gold")
        ctx.setTag("building:material", "metal")

    if ctx.getTag("building:part") == "column_pre":
        if ctx.current_object.split_index%2 == 0:
            ctx.scale(ctx.scope_sy(), "'1")
            #ctx.scale("'1.2", "'1.2")
            ctx.split_z_preserve_roof((
                (ctx.scope_sx() / 6, "column_base"),
                ("~1", "column_shaft"),
                (ctx.scope_sx()/4,"column_capitel"),
                (ctx.scope_sx()/16,"column_capitel1")))
        else:
            ctx.nil()

    if ctx.getTag("building:part") == "column_base":
        ctx.split_z_preserve_roof((
                ("~1", "column_base1"),
                ("~2", "column_base2") ))

    if ctx.getTag("building:part") == "column_base1":
        ctx.scale("'1.05", "'1.05")

    if ctx.getTag("building:part") == "column_base2":
        ctx.scale("'1.05", "'1.05")
        ctx.primitiveCylinder()

    if ctx.getTag("building:part") == "column_shaft":
        ctx.primitiveCylinder()
        ctx.scale("'0.9","'0.9")

    if ctx.getTag("building:part") == "column_capitel":
        ctx.scale("'1.25", "'1")

    if ctx.getTag("building:part") == "column_capitel1":
       ctx.scale("'0.95", "'0.95")

    if ctx.getTag("building:part") == "nil":
        ctx.nil()