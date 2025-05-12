# Projeto 2

![Sala de estar com mesa de café com tabuleiro de xadrez, próximo a um sofá e janela com uma
árvore logo afora](imgs/snapshot_2025-05-11_23-35-21.png)

Demonstração de um programa simples para a renderização de cenários 3D à partir
da importação de modelos em arquivos `.obj`

> Autor: Guilherme de Abreu Barreto, nUSP: 12543033

## ▶️ Como Executar

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

## 🕹️ Controles Interativos

### ⌨️ Teclado

| Tecla                         | Ação do Objeto Selecionado        | Ação da Câmera         |
| ----------------------------- | --------------------------------- | ---------------------- |
| **<kbd>w</kbd>/<kbd>s</kbd>** | -                                 | Mover frente/trás      |
| **<kbd>a</kbd>/<kbd>d</kbd>** | -                                 | Mover esquerda/direita |
| **<kbd>q</kbd>/<kbd>e</kbd>** | -                                 | Mover cima/baixo       |
| **<kbd>1</kbd>-<kbd>0</kbd>** | Selecionar objeto 1 a 10          | -                      |
| **<kbd>z</kbd>/<kbd>x</kbd>** | Ciclar objetos (anterior/próximo) | -                      |
| **<kbd>t</kbd>/<kbd>g</kbd>** | Mover longe/perto                 | -                      |
| **<kbd>f</kbd>/<kbd>h</kbd>** | Mover esquerda/direita            | -                      |
| **<kbd>r</kbd>/<kbd>y</kbd>** | Mover cima/baixo                  | -                      |
| **<kbd>u</kbd>/<kbd>o</kbd>** | Rotacionar no eixo Z (rolagem)    | -                      |
| **<kbd>i</kbd>/<kbd>k</kbd>** | Rotacionar no eixo X (inclinação) | -                      |
| **<kbd>j</kbd>/<kbd>l</kbd>** | Rotacionar no eixo Y (giro)       | -                      |
| **<kbd>c</kbd>/<kbd>v</kbd>** | Diminuir/aumentar escala          | -                      |
| **<kbd>p</kbd>**              | Alternar modo wireframe           | -                      |
| **<kbd>b</kbd>**              | Resetar transformações            | -                      |
| **<kbd>esc</kbd>**            | Fechar aplicação                  | -                      |

### 🖱️Mouse ou Touchpad

| Ação         | Efeito            |
| ------------ | ----------------- |
| **Arrastar** | Rotacionar câmera |
| **Scroll**   | Zoom in/out       |

> [!TIP]
>
> 1. O objeto selecionado aparece destacado no console
> 2. Modo wireframe (<kbd>p</kbd>) exibe apenas a estrutura poligonal
> 3. Reset (<kbd>b</kbd>) volta posição/rotação/escala para os valores iniciais
> 4. Movimentos da câmera são relativos à sua orientação atual

## Averiguação

O atual estado dos objetos pode ser acompanhado em uma tabela emitida ao
console, atualizada toda vez que ocorre uma mudança neste.

![Janela do programa ao lado de um terminal. O terminal exibe uma
tabelas que descrevem o atual estado da câmera e dos objetos apresentados na cena em termos
dos valores aplicados a transformações destes](imgs/snapshot_2025-05-12_00-13-54.png)
