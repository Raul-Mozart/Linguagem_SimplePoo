stateDiagram-v2
    [*] --> q0
    q0 --> q1 : qualquer char inválido (ex: @, #, $)
    q1 --> [*]