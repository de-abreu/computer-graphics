# Projeto 1

![Peças de xadrez de cores variadas, em posição de xeque-mate sobre um
tabulerio](imgs/snapshot_2025-04-06_20-03-00.png)

Demonstração de um programa simples para renderização de objetos em 2D e 3D, em
diferentes cores.

> Autor: Guilherme de Abreu Barreto, nUSP: 12543033

## Para executar o programa

### Usando Nix Flakes

Este projeto faz uso de [Nix Flakes](https://nixos.wiki/wiki/flakes) para a
instalação de dependências em um ambiente, para execução e desenvolvimento,
isolado. Um usuário que possui o gerenciador de pacotes Nix com Flakes
habilitados pode executar o programa com o comando:

```bash
nix run
```

E acessar um ambiente de desenvolvimento com:

```bash
nix develop
```

Pacotes instalados desta forma estão sujeitos a
[garbage collection](https://nix.dev/manual/nix/2.28/package-management/garbage-collection.html),
de forma a não poluir o sistema do usuário se usados apenas ocasionalmente.

### Usando `pip`

As dependências do projeto podem ser instaladas utilizando o gerenciador de
pacotes [`pip`](https://pypi.org/project/pip/) com o seguinte commando:

```bash
pip install -r requirements.txt
```

Em seguida o programa poderá ser executado com:

```bash
python src/main.py
```

## Instruções de uso

Os seguintes comandos foram mapeados ao teclado para a manipulação dos objetos
vistos em cena:

- Movimentação:

  - <kbd>w</kbd> mover para frente (-z);
  - <kbd>s</kbd> mover para trás (+z);
  - <kbd>a</kbd> mover para esquerda (-x);
  - <kbd>d</kbd> mover para direita(+x);
  - <kbd>r</kbd> mover para cima (+y);
  - <kbd>f</kbd> mover para baixo (-y);

- Escala:

  - <kbd>z</kbd> mover para diminuir tamanho;
  - <kbd>x</kbd> mover para aumentar tamanho;

- Rotação:

  - <kbd>i</kbd> rotaciona no sentido horário no eixo x;
  - <kbd>k</kbd> rotaciona no sentido anti-horário no eixo x;
  - <kbd>u</kbd> rotaciona no sentido horário no eixo y;
  - <kbd>o</kbd> rotaciona no sentido anti-horário no eixo y;
  - <kbd>l</kbd> rotaciona no sentido horário no eixo z;
  - <kbd>j</kbd> rotaciona no sentido anti-horário no eixo z;

- Reinicialização:

  - <kbd>y</kbd> retorna o objeto a sua posição inicial;

- Visualização:

  - <kbd>p</kbd> alterna entre visualizar objetos com ou sem preenchimento.

- Seleção:
  - <kbd>t</kbd> seleciona próximo objeto para controle;
  - <kbd>g</kbd> seleciona objeto anterior;

## Averiguação

O atual estado dos objetos pode ser acompanhado em uma tabela emitida ao
console, atualizada toda vez que ocorre uma mudança neste.

![Janela do tabuleiro e peças ladeada por um terminal. O terminal exibe uma
tabela que descreve o atual estado dos objetos apresentados na cena em termos
dos valores aplicados a transformações destes](imgs/snapshot_2025-04-07_11-07-43.png)
