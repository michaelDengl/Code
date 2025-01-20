using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;

public static class TaskFunction
{
    [FunctionName("AddTask")]
    public static async Task<IActionResult> AddTask(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "tasks")] HttpRequest req,
        ILogger log)
    {
        log.LogInformation("Adding a new task.");

        string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
        TaskItem data = JsonConvert.DeserializeObject<TaskItem>(requestBody);

        // Save the task to Azure Table Storage, Cosmos DB, or any other service here.
        log.LogInformation($"Task added: {data?.Description}");

        return new OkObjectResult(data);
    }

    [FunctionName("GetTasks")]
    public static async Task<IActionResult> GetTasks(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "tasks")] HttpRequest req,
        ILogger log)
    {
        log.LogInformation("Getting all tasks.");

        // Retrieve tasks from Azure Storage or another service.
        var tasks = new[] { new TaskItem { Description = "Example task", IsCompleted = false } };

        return new OkObjectResult(tasks);
    }
}

public class TaskItem
{
    public string Description { get; set; }
    public bool IsCompleted { get; set; }
}
