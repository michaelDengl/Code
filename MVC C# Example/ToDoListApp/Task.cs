using System;
using System.Collections.Generic;

//Model

namespace ToDoListApp
{
    public class Task
    {
        public string Description { get; set; }
        public bool IsCompleted { get; set; }
    }

    public class TaskManager
    {
        public List<Task> Tasks { get; private set; } = new List<Task>();

        public void AddTask(string description)
        {
            Tasks.Add(new Task { Description = description, IsCompleted = false });
        }

        public void MarkTaskCompleted(int index)
        {
            if (index >= 0 && index < Tasks.Count)
            {
                Tasks[index].IsCompleted = true;
            }
        }

        public void DeleteTask(int index)
        {
            if (index >= 0 && index < Tasks.Count)
            {
                Tasks.RemoveAt(index);
            }
        }
    }
}
