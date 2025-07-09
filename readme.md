# TechMatch

-> Sistema para processamento de currículos com assistencia de I.A. 

Interface está disponível em https://techmatch.public.metaespace.com:4443

O Swagger com a documentação da API está disponível em https://techmatch.public.metaespace.com:4443/docs

### Sobre o projeto:

- O projeto utiliza FastAPI, MongoDB e vLLM.
- Para interação com o MongoDB é utilizado o ODM (Object Document Model) [Beanie](https://beanie-odm.dev/).
- A parte do Front-end foi simplificada para apenas um template, devido a restrição de tempo do projeto.
- O Projeto é encapsulado em docker, e docker-compose, a definição está na pasta infra/dev/docker-compose.yml 

### Instruções de desenvolvimento

Para executar o projeto, utilize: 

```make run```

(Alias para docker-compose -f infra/dev/docker-compose.yml up -d --build)

Para parar o projeto execute: 

```make down``` 

(Alias para docker-compose -f infra/dev/docker-compose.yml down)

Outros alias estão presentes no Makefile, como shell para container do aplicativo e monitoramento dos logs.



