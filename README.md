# 🚗 Road Lane Detection with OpenCV

## Este projeto tem como objetivo a detecção de faixas de trânsito utilizando técnicas clássicas de Visão Computacional, com foco no método de Hoght Probabilistic.

### A abordagem se baseia na extração de padrões de cor e bordas, que permitem identificar segmentos de reta correspondentes às faixas da estrada.

## Metodologia

Para detectar as faixas, foi utilizado o Hough Transform Probabilístico (HoughLinesP), que retorna segmentos de linhas ao invés de linhas infinitas.

O algoritmo funciona a partir das bordas detectadas na imagem e identifica padrões geométricos lineares, entregando as coordenadas (x1, y1, x2, y2) de cada linha detectada, sendo depois separada matematicamente em linhas esquerdas e direitas

##  Pipeline de Processamento da Imagem:


### Grayscale 

* Conversão da imagem para tons de cinza
* Reduz a dimensionalidade, de 3 canais RBG para apenas 1
* Facilita a detecção de bordas 

### Gaussian Blur

* Aplicação de desfoque gaussiano.
* Reduz ruídos e suaviza a imagem, evitando bordas falsas.
  * Busca a normalização entre pixels vizinhos 

### Canny Edge Detection

* Identificação das bordas com base no gradiente de magnitude
* Etapa essencial para a aplicação  do Hough

### Region of Interest (ROI)

* Seleção da região relevante da imagem (onde a estrada está, tendo a baixa variação de posição).
* Evita a detecção de linhas irrelevante para a detecção da faixas

### Hough Transform Probabilístico

* Detecção das linhas a partir das bordas.
* Retorna segmentos de reta que representam as faixas da estrada.

## Tecnologias Utilizadas

Python

OpenCV

NumPy

## Observação

Neste projeto utilizei métodos clássicos, sem redes neurais, sendo ideal para compreender:

* Detecção de bordas
* Extração de features
* Funcionamento de ferramentas de pré-processamento e filtragem de imagens


Extração de features geométricas

Fundamentos de visão computacional
