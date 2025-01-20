namespace ToDoListApp
{
    partial class MainForm
    {
        private System.Windows.Forms.ListBox lstTasks;
        private System.Windows.Forms.TextBox txtTaskDescription;
        private System.Windows.Forms.Button btnAddTask;
        private System.Windows.Forms.Button btnMarkCompleted;
        private System.Windows.Forms.Button btnDeleteTask;

        private void InitializeComponent()
        {
            this.lstTasks = new System.Windows.Forms.ListBox();
            this.txtTaskDescription = new System.Windows.Forms.TextBox();
            this.btnAddTask = new System.Windows.Forms.Button();
            this.btnMarkCompleted = new System.Windows.Forms.Button();
            this.btnDeleteTask = new System.Windows.Forms.Button();
            this.SuspendLayout();

            // lstTasks
            this.lstTasks.Location = new System.Drawing.Point(12, 12);
            this.lstTasks.Size = new System.Drawing.Size(360, 200);

            // txtTaskDescription
            this.txtTaskDescription.Location = new System.Drawing.Point(12, 220);
            this.txtTaskDescription.Size = new System.Drawing.Size(260, 23);

            // btnAddTask
            this.btnAddTask.Location = new System.Drawing.Point(280, 220);
            this.btnAddTask.Size = new System.Drawing.Size(92, 23);
            this.btnAddTask.Text = "Add Task";
            this.btnAddTask.Click += new System.EventHandler(this.btnAddTask_Click);

            // btnMarkCompleted
            this.btnMarkCompleted.Location = new System.Drawing.Point(12, 260);
            this.btnMarkCompleted.Size = new System.Drawing.Size(360, 23);
            this.btnMarkCompleted.Text = "Mark Selected Task as Completed";
            this.btnMarkCompleted.Click += new System.EventHandler(this.btnMarkCompleted_Click);

            // btnDeleteTask
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
            this.ResumeLayout(false);
        }
    }
}
