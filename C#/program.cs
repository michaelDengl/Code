using System;
using System.Collections.Generic;

class Program
{
    static void Main(string[] args)
    {
        List<Task> tasks = new List<Task>();
        string input;

        do
        {
            Console.Clear();
            Console.WriteLine("To-Do List Manager");
            Console.WriteLine("1. View Tasks");
            Console.WriteLine("2. Add Task");
            Console.WriteLine("3. Mark Task as Completed");
            Console.WriteLine("4. Exit");
            Console.Write("Choose an option: ");

            input = Console.ReadLine();

            switch (input)
            {
                case "1":
                    ViewTasks(tasks);
                    break;
                case "2":
                    AddTask(tasks);
                    break;
                case "3":
                    MarkTaskCompleted(tasks);
                    break;
                case "4":
                    Console.WriteLine("Exiting...");
                    break;
                default:
                    Console.WriteLine("Invalid option. Press any key to try again.");
                    Console.ReadKey();
                    break;
            }
        } while (input != "4");
    }

    static void ViewTasks(List<Task> tasks)
    {
        Console.Clear();
        Console.WriteLine("Tasks:");

        if (tasks.Count == 0)
        {
            Console.WriteLine("No tasks available.");
        }
        else
        {
            for (int i = 0; i < tasks.Count; i++)
            {
                var status = tasks[i].IsCompleted ? "[Completed]" : "[Pending]";
                Console.WriteLine($"{i + 1}. {tasks[i].Description} {status}");
            }
        }

        Console.WriteLine("\nPress any key to return to the main menu...");
        Console.ReadKey();
    }

    static void AddTask(List<Task> tasks)
    {
        Console.Clear();
        Console.Write("Enter task description: ");
        string description = Console.ReadLine();

        if (!string.IsNullOrWhiteSpace(description))
        {
            tasks.Add(new Task { Description = description, IsCompleted = false });
            Console.WriteLine("Task added successfully!");
        }
        else
        {
            Console.WriteLine("Task description cannot be empty.");
        }

        Console.WriteLine("\nPress any key to return to the main menu...");
        Console.ReadKey();
    }

    static void MarkTaskCompleted(List<Task> tasks)
    {
        Console.Clear();
        Console.WriteLine("Mark Task as Completed");

        if (tasks.Count == 0)
        {
            Console.WriteLine("No tasks available.");
        }
        else
        {
            for (int i = 0; i < tasks.Count; i++)
            {
                var status = tasks[i].IsCompleted ? "[Completed]" : "[Pending]";
                Console.WriteLine($"{i + 1}. {tasks[i].Description} {status}");
            }

            Console.Write("\nEnter task number to mark as completed: ");
            if (int.TryParse(Console.ReadLine(), out int taskNumber) && taskNumber > 0 && taskNumber <= tasks.Count)
            {
                tasks[taskNumber - 1].IsCompleted = true;
                Console.WriteLine("Task marked as completed!");
            }
            else
            {
                Console.WriteLine("Invalid task number.");
            }
        }

        Console.WriteLine("\nPress any key to return to the main menu...");
        Console.ReadKey();
    }
}

class Task
{
    public string Description { get; set; }
    public bool IsCompleted { get; set; }
}
