using System;
using System.Windows.Forms;

namespace ToDoListApp
{
    public partial class MainForm : Form
    {
        private TaskManager taskManager = new TaskManager();

        public MainForm()
        {
            InitializeComponent();
            UpdateTaskList();
        }

        private void btnAddTask_Click(object sender, EventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(txtTaskDescription.Text))
            {
                taskManager.AddTask(txtTaskDescription.Text);
                txtTaskDescription.Clear();
                UpdateTaskList();
            }
        }

        private void btnMarkCompleted_Click(object sender, EventArgs e)
        {
            if (lstTasks.SelectedIndex >= 0)
            {
                taskManager.MarkTaskCompleted(lstTasks.SelectedIndex);
                UpdateTaskList();
            }
        }

        private void btnDeleteTask_Click(object sender, EventArgs e)
        {
            if (lstTasks.SelectedIndex >= 0)
            {
                taskManager.DeleteTask(lstTasks.SelectedIndex);
                UpdateTaskList();
            }
            else
            {
                MessageBox.Show("Please select a task to delete.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void UpdateTaskList()
        {
            lstTasks.Items.Clear();
            foreach (var task in taskManager.Tasks)
            {
                string status = task.IsCompleted ? "[Completed]" : "[Pending]";
                lstTasks.Items.Add($"{task.Description} {status}");
            }
        }
    }
}
