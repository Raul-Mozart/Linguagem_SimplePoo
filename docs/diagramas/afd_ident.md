```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1 : letra, _
    q1 --> q1 : letra, dígito, _
    q1 --> [*]
```