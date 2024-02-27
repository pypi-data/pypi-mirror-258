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


def responsePayload():
    return """
using System.Reflection.Metadata;
using Category.Application.Interfaces;

namespace Category.Application.Dtos
{
    public class Response : IResponse
    {
        public bool Success { get; set; }

        public ICollection<string> Messages { get; set; }

        public Response(bool success, params string[] messages)
        {
            this.Success = success;

            if (messages != null)
                this.Messages = new List<string>(messages);
        }

        public Response(params string[] messages)
            : this(true, messages)
        {
        }
    }

    public class Response<TViewModel> : Response, IResponse<TViewModel>
        where TViewModel : class
    {
        public TViewModel Data { get; set; }

        public Response(bool success = true, params string[] messages)
            : base(success, messages)
        {
        }

        public Response(bool success = true, TViewModel data = null, params string[] messages)
            : this(success, messages)
        {
            this.Data = data;
        }

        public Response(TViewModel data = null, params string[] messages)
            : this(true, data, messages)
        {
        }

        public Response(TViewModel data = null)
            : this(data, null)
        {
        }
    }
}
    """


def responseArrayPayload():
    return """
using System.Reflection.Metadata;
using Category.Application.Interfaces;

namespace Category.Application.Dtos
{
public class ResponseArray<TResponse> : Response, IResponseArray<TResponse>

    {

        public long Length { get; set; }

        public IEnumerable<TResponse> Data { get; set; }

        public ResponseArray(long length, IEnumerable<TResponse> data)

        {

            this.Length = length;

            this.Data = data;

        }

        public ResponseArray(IEnumerable<TResponse> data)

            : this(data.Count(), data)

        {

        }

    }
}"""


def responseInterfacePayload():
    return """
using Newtonsoft.Json;

namespace Category.Application.Interfaces
{
    public interface IResponse
    {
        /// <summary>
        /// Informa se a requisição foi retornada com sucesso
        /// </summary>
        [JsonProperty]
        [JsonRequired]
        bool Success { get; set; }

        /// <summary>
        /// Mensagens de retorno
        /// </summary>
        [JsonProperty]
        ICollection<string> Messages { get; set; }
    }

    public interface IResponse<TResponse> : IResponse
         where TResponse : class
    {
        /// <summary>
        /// Valor a ser retornado
        /// </summary>
        [JsonProperty]
        TResponse Data { get; set; }
    }
}"""


def responseArrayInterfacePayload():
    return """
using Newtonsoft.Json;

namespace Category.Application.Interfaces
{
    public interface IResponseArray<TResponse> : IResponse
    {
        /// <summary>
        /// Quantidade de registros existentes
        /// Quantidade usada para paginação do sistema
        /// </summary>
        [JsonProperty]
        [JsonRequired]
        long Length { get; set; }

        /// <summary>
        /// Registros retornados na consulta
        /// </summary>
        [JsonProperty]
        [JsonRequired]
        IEnumerable<TResponse> Data { get; set; }
    }
}"""
