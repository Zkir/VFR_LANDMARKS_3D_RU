/*
 * This is draft grammar for PML language for blender-osm plugin
 * (c) Zkir 2019, all rights reserved. 
 */

grammar PML;
style_file
    : (rule_definition|fragment_definition)+
    ; 

rule_definition
    :rule_head LCURLY rule_body RCURLY
    ;

fragment_definition
    :fragment_head LCURLY rule_body RCURLY
    ; 

rule_head
    :element_name (LBRACK condition RBRACK)?
    ; 

fragment_head
    :element_name STRUDEL fragment_name //(LBRACK condition RBRACK)?
    //OPEN QUESTION. Can fragment have condition clause? 
    ; 

rule_body
    :attribute* (LBRACK markup RBRACK)?
    ; 

markup
    : rule_definition+
    ;

condition
    :selector
    |IDENTIFIER EQUAL (string_literal|number)
    ;

element_name
    : IDENTIFIER
    ; 

fragment_name
    : IDENTIFIER
    ; 
selector
    : IDENTIFIER
    ; 

attribute
    : attribute_name COLON attribute_value (PIPE attribute_value)* SEMI
    ;         

attribute_name
    : IDENTIFIER
    ; 

attribute_value
    : simple_attr_value
    | number IDENTIFIER //number could be followed by some descriptor, say, offset: 0.5 layer
    | IDENTIFIER+  //Could be serveral descriptors, say, red brick
    ;

simple_attr_value
    :number|string_literal|IDENTIFIER|function_call
    ;

function_call
    : function_name LPAREN simple_attr_value (COMMA simple_attr_value)*  RPAREN
    ;
function_name
    : IDENTIFIER
    ;

number
    : NUMBER
    ; 

string_literal
    : STRING_LITERAL
    ;

//******************************************************************************
//Lexer rules
//******************************************************************************

//ELEMENT_NAME:'footprint'|'facade'|'level'|'window'|'div'|'roof_side'|'ridge';
IDENTIFIER
    : [a-zA-Z]([a-zA-Z0-9_]|'-')*  //[a-zA-Z][a-zA-Z0-9_]*
    ;

STRING_LITERAL
    : '"' ('""' | ~ ('"'))* '"'
    ;

NUMBER
    : ('0' .. '9') + (('.' ('0' .. '9') + )? )
    ;  

STRUDEL:    '@';
LCURLY:     '{';
RCURLY:     '}';
LPAREN:     '(' ;
RPAREN:     ')' ;
LBRACK:     '[';
RBRACK:     ']';
PIPE:       '|';
EQUAL:      '=';
COMMA:      ',' ;
COLON:      ':'; 
SEMI:       ';'; 


//Boolean  operators
//NOT:        'not';
//OR:         'or';
//AND:        'and';


COMMENT
   :'//' .*? [\r\n] -> skip 
   ;  

WS : [ \t\r\n]+ -> skip ;
