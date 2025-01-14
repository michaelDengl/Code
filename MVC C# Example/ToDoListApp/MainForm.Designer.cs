using System.Windows.Forms;

//Partial View

namespace ToDoListApp
{
    partial class MainForm
    {
        private ListBox lstTasks;
        private TextBox txtTaskDescription;
        private Button btnAddTask;
        private Button btnMarkCompleted;
        private Button btnDeleteTask;

        private void InitializeComponent()
        {
            this.lstTasks = new ListBox();
            this.txtTaskDescription = new TextBox();
            this.btnAddTask = new Button();
            this.btnMarkCompleted = new Button();
            this.btnDeleteTask = new Button();

            // ListBox
            this.lstTasks.Location = new System.Drawing.Point(12, 12);
            this.lstTasks.Size = new System.Drawing.Size(360, 200);

            // TextBox
            this.txtTaskDescription.Location = new System.Drawing.Point(12, 220);
            this.txtTaskDescription.Size = new System.Drawing.Size(260, 23);

            // Add Task Button
            this.btnAddTask.Location = new System.Drawing.Point(280, 220);
            this.btnAddTask.Size = new System.Drawing.Size(92, 23);
            this.btnAddTask.Text = "Add Task";
            this.btnAddTask.Click += new System.EventHandler(this.btnAddTask_Click);

            // Mark Completed Button
            this.btnMarkCompleted.Location = new System.Drawing.Point(12, 260);
            this.btnMarkCompleted.Size = new System.Drawing.Size(360, 23);
            this.btnMarkCompleted.Text = "Mark Selected Task as Completed";
            this.btnMarkCompleted.Click += new System.EventHandler(this.btnMarkCompleted_Click);

            // Delete Task Button
            this.btnDeleteTask.Location = new System.Drawing.Point(12, 290);
            this.btnDeleteTask.Size = new System.Drawing.Size(360, 23);
            this.btnDeleteTask.Text = "Delete Selected Task";
            this.btnDeleteTask.Click += new System.EventHandler(this.btnDeleteTask_Click);

            // MainForm
            this.ClientSize = new System.Drawing.Size(384, 331);
            this.Controls.Add(this.lstTasks);
            this.Controls.Add(this.txtTaskDescription);
            this.Controls.Add(this.btnAddTask);
            this.Controls.Add(this.btnMarkCompleted);
            this.Controls.Add(this.btnDeleteTask);
            this.Text = "To-Do List Manager";
        }
    }
}
