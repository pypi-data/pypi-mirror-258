import{s as e}from"./simple-mode-C4imR_6Q.js";const n=e({start:[{regex:/#?!.*/,token:"comment"},{regex:/"""/,token:"string",next:"string3"},{regex:/(STRING:)(\s)/,token:["keyword",null],next:"string2"},{regex:/\S*?"/,token:"string",next:"string"},{regex:/(?:0x[\d,a-f]+)|(?:0o[0-7]+)|(?:0b[0,1]+)|(?:\-?\d+.?\d*)(?=\s)/,token:"number"},{regex:/((?:GENERIC)|\:?\:)(\s+)(\S+)(\s+)(\()/,token:["keyword",null,"def",null,"bracket"],next:"stack"},{regex:/(M\:)(\s+)(\S+)(\s+)(\S+)/,token:["keyword",null,"def",null,"tag"]},{regex:/USING\:/,token:"keyword",next:"vocabulary"},{regex:/(USE\:|IN\:)(\s+)(\S+)(?=\s|$)/,token:["keyword",null,"tag"]},{regex:/(\S+\:)(\s+)(\S+)(?=\s|$)/,token:["keyword",null,"def"]},{regex:/(?:;|\\|t|f|if|loop|while|until|do|PRIVATE>|<PRIVATE|\.|\S*\[|\]|\S*\{|\})(?=\s|$)/,token:"keyword"},{regex:/\S+[\)>\.\*\?]+(?=\s|$)/,token:"builtin"},{regex:/[\)><]+\S+(?=\s|$)/,token:"builtin"},{regex:/(?:[\+\-\=\/\*<>])(?=\s|$)/,token:"keyword"},{regex:/\S+/,token:"variable"},{regex:/\s+|./,token:null}],vocabulary:[{regex:/;/,token:"keyword",next:"start"},{regex:/\S+/,token:"tag"},{regex:/\s+|./,token:null}],string:[{regex:/(?:[^\\]|\\.)*?"/,token:"string",next:"start"},{regex:/.*/,token:"string"}],string2:[{regex:/^;/,token:"keyword",next:"start"},{regex:/.*/,token:"string"}],string3:[{regex:/(?:[^\\]|\\.)*?"""/,token:"string",next:"start"},{regex:/.*/,token:"string"}],stack:[{regex:/\)/,token:"bracket",next:"start"},{regex:/--/,token:"bracket"},{regex:/\S+/,token:"meta"},{regex:/\s+|./,token:null}],languageData:{name:"factor",dontIndentStates:["start","vocabulary","string","string3","stack"],commentTokens:{line:"!"}}});export{n as factor};
