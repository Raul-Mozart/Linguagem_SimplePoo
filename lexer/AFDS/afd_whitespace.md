stateDiagram-v2
    [*] --> q0
    q0 --> q1 : espaço, \t, \r, \n
    q1 --> q1 : espaço, \t, \r, \n
    q1 --> [*]