/*
 
 * This is ANTLR grammar for CGA language of ESRI CityEngine tool
 * (c) Zkir 2019, all rights reserved. 
 
*/

grammar CGA;
cga
    :statement+
    ;

statement
    : version 
    | import_lib  
    | attr_declr  
    | const_declr
    | rule_declr
    | func_declr  
    ;    

version
    : VERSION string 
    ; 

import_lib
    : IMPORT identifier COLON string  //import lib_alias : lib_path
    ;

//attr TotalHeight=20
attr_declr
    : annotatation* ATTR identifier ASSIGNMENT expr_simple 
    ; 

const_declr
    : annotatation* CONST identifier ASSIGNMENT expr_simple 
    ; 

rule_declr
    : annotatation* rule_head ARROW rule_body
    ;             
annotatation
    : STRUDEL identifier
    ;    

rule_head
    : identifier  (LPAREN formal_parameter_list RPAREN)?
    ; 
rule_body
    : operation+
    //| (CASE expr comparison_operator expr  COLON operation+)+ (ELSE COLON operation+)?  
    | (CASE expr  COLON rule_body)+ (ELSE COLON rule_body)?  
    ;
func_declr
    : annotatation* identifier (LPAREN formal_parameter_list RPAREN) ASSIGNMENT expr_simple 
    ;
operation
    : identifier (LPAREN parameter_list RPAREN)? markup?
    | push=LBRACK // Push and pop operations ([/]) are considered as operations here. 
    | pop=RBRACK // No check for evenness.  
    ;

formal_parameter_list
    : identifier (COMMA identifier)*
    ;

parameter_list
    : expr (COMMA expr)*
    ;
 
markup
    : LCURLY markup_block (PIPE markup_block)* RCURLY MULT?
    ;    

markup_block
    : expr COLON rule_body
    | expr ASSIGNMENT rule_body  
    ;
//=

expr
    : expr_simple
    | APROX expr_simple  
    | REL expr_simple  
    ; 

expr_simple
    : const_expr  
    | identifier    
    | func_call  
    | PLUS expr_simple  
    | MINUS expr_simple    
    | LPAREN  expr_simple RPAREN
    | expr_simple MULT expr_simple  
    | expr_simple DIV  expr_simple  
    | expr_simple PLUS expr_simple  
    | expr_simple MINUS expr_simple  
    | expr_simple comparison_operator expr_simple   //Not sure about priority in CGA
    | NOT expr_simple                               //what has more priority , 
    | expr_simple AND expr_simple                   //boolean or comparison
    | expr_simple OR expr_simple  
    
    ;

func_call
    :identifier LPAREN  (expr_simple (COMMA expr_simple)*)? RPAREN  
    ;

const_expr
    : number 
    | string   
    | bool 
    ;

string
    : STRING_LITERAL
    ;

number
    :NUMBER
    ;

bool
    : TRUE | FALSE
    ;  

identifier 
    :IDENT
    ;

comparison_operator
   : EQUAL
   | NOT_EQUAL
   | LT
   | LE
   | GE
   | GT
   ;

//Keywords
ARROW:   '-->'; 
VERSION: 'version';
IMPORT:  'import';
ATTR:    'attr';
CONST:   'const';
CASE:    'case';
ELSE:    'else';

//special values
TRUE:  'true' ;
FALSE: 'false'; //Should stand higher that ID_MX

// Identifier
//It can be simple identifier: A123 or complex: world.up
IDENT: ID_MX1 | ID_MX1 '.' ID_MX1; 
fragment ID_MX1: [a-zA-Z][a-zA-Z0-9_]*;

STRING_LITERAL
   : '"' ('""' | ~ ('"'))* '"'
   ;

NUMBER
   : ('0' .. '9') + (('.' ('0' .. '9') + )? )
   ;

COLON:      ':';   
ASSIGNMENT: '=';
COMMA:      ',' ;
STRUDEL:    '@';
LCURLY:     '{';
RCURLY:     '}';
LPAREN:     '(' ;
RPAREN:     ')';
LBRACK:     '[';
RBRACK:     ']';
PIPE:       '|';
REL:        '\''; //Single Quote is used as relative operator
APROX:      '~';  //tilda is used as approximate operator

//Arithmetic operators
PLUS:       '+';
MINUS:      '-';
MULT:       '*';
DIV:        '/';

//Comparision operators
EQUAL     : '==';
NOT_EQUAL : '!=';
LT        : '<';
LE        : '<=';
GE        : '>=';
GT        : '>';

//Boolean  operators
NOT:        '!';
OR:         '||';
AND:        '&&';



COMMENT_1
   : '/*' .*? '*/' -> skip
   ;

COMMENT_2
   :'#' .*? [\r\n] -> skip 
   ;  
COMMENT_3
   :'//' .*? [\r\n] -> skip 
   ;  


WS : [ \t\r\n]+ -> skip ;