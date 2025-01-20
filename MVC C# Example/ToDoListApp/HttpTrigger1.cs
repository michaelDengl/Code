using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

public static class HttpTrigger1
{
    [FunctionName("AddTask")]
    public static async Task<IActionResult> AddTask(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "task")] HttpRequest req,
        [CosmosDB(
            databaseName: "mytodolistdb",
            collectionName: "Tasks",
            ConnectionStringSetting = "CosmosDBConnectionString")] IAsyncCollector<dynamic> tasks,
        ILogger log)
    {
        log.LogInformation("Processing AddTask request.");

        string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
        dynamic task = JsonConvert.DeserializeObject(requestBody);

        if (task == null || string.IsNullOrWhiteSpace((string)task.title))
        {
            return new BadRequestObjectResult("Invalid task data.");
        }

        task.id = Guid.NewGuid().ToString();
        await tasks.AddAsync(task);

        return new OkObjectResult(task);
    }
}
