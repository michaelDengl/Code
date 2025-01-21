using System.IO;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;

public class TaskFunction
{
    private readonly ILogger<TaskFunction> _logger;

    public TaskFunction(ILogger<TaskFunction> logger)
    {
        _logger = logger;
    }

    [Function("AddTask")]
    public async Task<HttpResponseData> AddTask(
        [HttpTrigger(AuthorizationLevel.Function, "post", Route = "tasks")] HttpRequestData req,
        [CosmosDBOutput(
            databaseName: "ToDoList",
            containerName: "Tasks",
            Connection = "CosmosDBConnectionString")] IAsyncCollector<TaskItem> taskItems)
    {
        _logger.LogInformation("AddTask function is initialized and running.");

        string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
        TaskItem data = JsonSerializer.Deserialize<TaskItem>(requestBody);

        if (data == null || string.IsNullOrWhiteSpace(data.Description))
        {
            var badRequestResponse = req.CreateResponse(System.Net.HttpStatusCode.BadRequest);
            await badRequestResponse.WriteStringAsync("Invalid task data.");
            return badRequestResponse;
        }

        data.Id = System.Guid.NewGuid().ToString();
        await taskItems.AddAsync(data);

        _logger.LogInformation($"Task added with ID: {data.Id}");
        var response = req.CreateResponse(System.Net.HttpStatusCode.OK);
        await response.WriteAsJsonAsync(data);
        return response;
    }

    [Function("GetTasks")]
    public async Task<HttpResponseData> GetTasks(
        [HttpTrigger(AuthorizationLevel.Function, "get", Route = "tasks")] HttpRequestData req,
        [CosmosDBInput(
            databaseName: "ToDoList",
            containerName: "Tasks",
            Connection = "CosmosDBConnectionString",
            SqlQuery = "SELECT * FROM c")] IEnumerable<TaskItem> taskItems)
    {
        _logger.LogInformation("GetTasks function is initialized and running.");

        var response = req.CreateResponse(System.Net.HttpStatusCode.OK);
        await response.WriteAsJsonAsync(taskItems);
        return response;
    }
}

public class TaskItem
{
    public string Id { get; set; }
    public string Description { get; set; }
}
