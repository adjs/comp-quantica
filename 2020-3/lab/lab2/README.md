# Lab2 - Realização de operadores controlados

## Objetivo:
- Implementar qualquer operador quântico sobre 1 qubit.
  - https://youtu.be/hvpGVdvGdek?t=148
- Construir operadores controlados utilizando operadores sobre um qubit e cx.
  - https://youtu.be/8thUIGA0Vf8?t=144
- Construir a porta Toffoli
  - https://youtu.be/sPx97N6sdCk?t=16
- Inicializar um estado quântico.
  - https://www.youtube.com/watch?v=orqohycxsYg
  - https://www.youtube.com/watch?v=jry-qcsOIpM
  - https://www.youtube.com/watch?v=ROv4Io2mlTo

## Questões
1. Dado uma matriz unitária V, determine os números reais `alpha`, `beta`, `gamma` e `delta` de modo que
```python
V = e^{1j*alpha} * Rz(beta) @ Ry(gamma) @ Rz(delta).
```



2. Dada uma matriz unitária V, construa um circuito para o operador V controlado. Nesta questão você pode utilizar apenas operadores sobre um qubit e cx.



3. Utilizando apenas operadores sobre um qubit e cx, construa um circuito quântico que tenha a ação do operador Toffoli.


4. Dado um vetor real com norma 1 e dimensão 8, construa um circuito que inicialize um estado quântico com amplitudes correspondendo às coordenadas do vetor.

5. Questão bônus. Dado um vetor complexo unitário. Inicialize um estado quântico com amplitudes correspondendo às coordenadas do vetor.

----------
- Vídeo sobre a decomposição RzRyRz https://youtu.be/hvpGVdvGdek?t=148

- Vídeo com a construção de operadores controlados https://youtu.be/8thUIGA0Vf8?t=144

- Circuito para implementação do operador Toffoli https://youtu.be/sPx97N6sdCk?t=16

- Inicialização de estados quânticos
