using Microsoft.Azure.Functions.Extensions.DependencyInjection;
using Microsoft.Azure.WebJobs.Extensions.CosmosDB;

[assembly: FunctionsStartup(typeof(ToDoListApp.Startup))]

namespace ToDoListApp
{
    public class Startup : FunctionsStartup
    {
        public override void Configure(IFunctionsHostBuilder builder)
        {
            // Add CosmosDB binding
            builder.AddCosmosDB();
        }
    }
}
