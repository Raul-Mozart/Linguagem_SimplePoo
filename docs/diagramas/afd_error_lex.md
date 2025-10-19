```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : "char inválido (@ # $ etc)"
    q1 --> [*]
```