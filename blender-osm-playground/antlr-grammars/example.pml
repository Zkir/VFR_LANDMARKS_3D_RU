footprint {
    levels: attr("building:levels") | random_weighted(4, 10, 5, 40, 6,10);
    roof-shape: gabled;
}

facade@brown_brick {
    cladding: brick brown;
}

level@staircase {
    offset: 0.5 level;
}

window@back_facade_window {
    width: 1.2;
    height: 1.8;
    panels: 1;
}

window@roof_window{
    width: 0.8;
    height: 0.8;
    rows: 1;
    panels: 1;
}

div@window_and_balcony{
    label: "Window and Balcony";
    [
    level{
        [
            window{
                width: 1.8;
                height: 2.10;
                rows: 1;
                panels: 2;
            }
            balcony{
            }
        ]
    }

    basement{
        [
            window{
                 width: 1;
                 height: 1;
                 rows: 1;
                 panels: 1;
            }
        ]
    }
    ]
}

div@staircase {
    use: staircase;
    label: "Staircase";
        [
           level {
               [
                    window{
                        width: 0.8;
                        height: 0.8;
                        rows: 1;
                        panels: 1;
                    }
               ]
           }
           level[i=0] {
               [
                   door{
                       label: "entrance door";
                   }
               ]
           }
        ]
}

div@roof_side {
    width: from(main_section);
    symmetry: rightmost-of-last;
}

facade[front] {
    use: brown_brick;
    symmetry: middle-of-last;
    symmetry-flip: flip;
    [
        div{
            use: window_and_balcony;
            id: main_section;
            label: "Window and Balcony";
        }
        div{
            use: staircase;
            label: "Staircase";
        }
    ]
}

facade[back] {
    use: brown_brick;
    symmetry: rightmost-of-last;
    [
        level {
            [
                balcony{}
                window{
                    use: back_facade_window;
                }
                window{
                    use: back_facade_window;
                }
            ] 
        }
    ]
}

roof_side[front] {
    [
        div{
            use: roof_side;
            [
                window{
                    use: roof_window;
                }
                window{
                    use: roof_window;
                }
            ]
         }
    ]
}

roof_side[back] {
    [
        div {
            use: roof_side;
            [
                Dormer{}
            ]
        }
     ]
}

ridge {
    [
        div {
            width: from(main_section);
            repeat: no;
            [
                chimney{}
            ]
        }
     ]
}