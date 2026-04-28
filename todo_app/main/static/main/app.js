const API = "/api";

class TaskApp {
    constructor() {
        this.taskList = document.getElementById("taskList");
        this.input = document.getElementById("taskInput");
        this.descriptionInput = document.getElementById("descriptionInput");
        this.addBtn = document.getElementById("addBtn");

        this.draggedId = null;
        this.editingId = null;

        // Infinite scroll state
        this.nextCursor = null;
        this.isLoading = false;
        this.hasMore = true;
        this.allTasks = []; // Keep track of all loaded tasks

        this.bindEvents(); 
        this.setupInfiniteScroll();
        this.loadTasks(); // Initial load of the tasks when the app starts
    }

    bindEvents() {
        this.addBtn.onclick = () => this.createTask();
    }

    setupInfiniteScroll() {
        this.taskList.addEventListener("scroll", () => {
            // Check if scrolled near bottom (within 200px)
            if (
                this.taskList.scrollTop + this.taskList.clientHeight >=
                this.taskList.scrollHeight - 200
            ) {
                if (!this.isLoading && this.hasMore) {
                    this.loadMoreTasks();
                }
            }
        });
    }

    // API CALLS
    async fetchTasks(cursor = null) {
        let url = `${API}/tasks/`;
        if (cursor) {
            url += `?cursor=${cursor}`;
        }
        const res = await fetch(url);
        return await res.json();
    }

    async createTask() {
        const title = this.input.value.trim();
        const description = this.descriptionInput.value.trim();
        if (!title) return;

        await fetch(`${API}/tasks/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description })
        });

        this.input.value = "";
        this.descriptionInput.value = "";
        // Reset pagination and reload from start
        this.nextCursor = null;
        this.allTasks = [];
        this.hasMore = true;
        this.loadTasks();
    }

    async updateTask(task) {
        this.editingId = task.id;

        // Note: Title cannot be empty.
        let title = prompt("Update task title:", task.title);
        if (title === null) return this.editingId = null;

        title = title.trim();
        if (!title) {
            alert("Title cannot be empty");
            return this.updateTask(task);
        }

        let description = prompt("Update task description:", task.description || "");
        if (description === null) return this.editingId = null;

        await fetch(`${API}/tasks/${task.id}/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description })
        });

        this.editingId = null;
        // Reset pagination and reload
        this.nextCursor = null;
        this.allTasks = [];
        this.hasMore = true;
        this.loadTasks();
    }

    async deleteTask(taskId) {
        if (!confirm("Delete this task?")) return;

        await fetch(`${API}/tasks/${taskId}/`, {
            method: "DELETE"
        });

        // Reset pagination and reload
        this.nextCursor = null;
        this.allTasks = [];
        this.hasMore = true;
        this.loadTasks();
    }

    async reorderTask(newIndex) {
        await fetch(`${API}/tasks/reorder/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id: this.draggedId,
                newIndex
            })
        });

        // Reset pagination and reload
        this.nextCursor = null;
        this.allTasks = [];
        this.hasMore = true;
        this.loadTasks();
    }

    // Load and render functions
    async loadTasks() {
        this.isLoading = true;
        const data = await this.fetchTasks();
        
        // Clear the list for fresh start
        this.allTasks = [];
        this.taskList.innerHTML = "";
        
        this.renderPage(data);
        this.isLoading = false;
    }

    async loadMoreTasks() {
        if (!this.nextCursor || this.isLoading) return;
        
        this.isLoading = true;
        const data = await this.fetchTasks(this.nextCursor);
        this.renderPage(data);
        this.isLoading = false;
    }

    renderPage(data) {
        // Handle paginated response format
        const tasks = data.results || data;
        
        tasks.forEach((task) => {
            this.allTasks.push(task);
            const li = this.createTaskElement(task, this.allTasks.length - 1);
            this.taskList.appendChild(li);
        });

        // Update pagination state
        this.nextCursor = data.next ? this.extractCursor(data.next) : null;
        this.hasMore = !!data.next;
    }

    extractCursor(nextUrl) {
        // Extract cursor parameter from next URL
        const url = new URL(nextUrl, window.location.origin);
        return url.searchParams.get('cursor');
    }

    createTaskElement(task, index) {
        const li = document.createElement("li");
        li.className = "task-item";

        const content = document.createElement("div");
        content.className = "task-content";

        const title = this.createTitle(task);
        const description = this.createDescription(task);

        content.appendChild(title);
        if (task.description) {
            content.appendChild(description);
        }

        const actions = document.createElement("div");
        actions.className = "task-actions";

        const editBtn = this.createEditButton(task);
        const deleteBtn = this.createDeleteButton(task);

        actions.appendChild(editBtn);
        actions.appendChild(deleteBtn);

        this.setupDrag(li, task, index);

        li.appendChild(content);
        li.appendChild(actions);

        return li;
    }

    createTitle(task) {
        const span = document.createElement("span");
        span.className = "task-title";
        span.textContent = task.title;
        return span;
    }

    createDescription(task) {
        const desc = document.createElement("p");
        desc.className = "task-description";
        desc.textContent = task.description;
        return desc;
    }

    createEditButton(task) {
        const btn = document.createElement("button");
        btn.textContent = "Edit";
        btn.onclick = () => this.updateTask(task);
        return btn;
    }

    createDeleteButton(task) {
        const btn = document.createElement("button");
        btn.textContent = "Delete";
        btn.onclick = () => this.deleteTask(task.id);
        return btn;
    }

    // This will set up the necessary drag-and-drop events for a task item created.
    setupDrag(li, task, index) {
        li.draggable = true;

        li.addEventListener("dragstart", () => {
            this.draggedId = task.id;
        });

        li.addEventListener("dragover", e => e.preventDefault());

        li.addEventListener("drop", () => {
            this.reorderTask(index);
        });
    }
}

new TaskApp();