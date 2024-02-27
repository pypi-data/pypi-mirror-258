def envPayload():
    return """
#ToDo: change to your APM credentials
ELASTIC_APM_SERVICE_NAME=teste_quatro
ELASTIC_APM_SERVER_URLS=http://localhost:8200
ELASTIC_APM_SECRET_TOKEN=hashToken
"""


def dockerFilePayload(solutionName: str):
    # TODO: change to dotnet 8.0
    return f"""
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
ARG VERSION
ARG ENVIRONMENT
ENV VERSION=$VERSION
ENV ENVIRONMENT=$ENVIRONMENT
ENV ASPNETCORE_URLS=http://*:80
ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgdiplus libc6-dev apt-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
RUN apt-get update && \ 
    apt-get install -y --no-install-recommends \
    clang zlib1g-dev 
WORKDIR /src
COPY . .
WORKDIR "/src/{solutionName}.Api"
RUN dotnet restore "{solutionName}.Api.csproj"
RUN dotnet build "{solutionName}.Api.csproj" -c Release -o /app/build --no-restore

FROM build AS publish
RUN dotnet publish "{solutionName}.Api.csproj" -c Release -o /app/publish --no-restore

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "{solutionName}.Api.dll"]
    """


def dockerIgnorePayload():
    return """
**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/azds.yaml
**/bin
**/charts
**/docker-compose*
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
LICENSE
README.md
"""
