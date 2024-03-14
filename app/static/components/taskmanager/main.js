// import TaskForm from '../taskform/main.js';
import TaskList from '../tasklist/main.js';
// customElements.define('task-form', TaskForm);
customElements.define('view-content', TaskList);

//MANAGER
export default class extends HTMLElement {
    // http://127.0.0.1:5000

    #shadow;
    #cssfile = "main.css";

    constructor() {
        // Always call super first in constructor
        super();

        // Entry point to the shadow DOM
        this.#shadow = this.attachShadow({mode: 'closed'});
        this.#createLink();
        this.#createHTML();
        //        this.#shadow.querySelector("task-list").setRemoveHandler(this.#deleteStudent.bind(this));
        //        this.#shadow.querySelector("task-form").setSendHandler(this.#addStudent.bind(this));

        // const taskform = this.#shadow.querySelector('task-form');
        const tasklist = this.#shadow.querySelector('view-content');

        // taskform.enableaddtask();

        // taskform.addtaskCallback(this.#addTask.bind(this));


        tasklist.deletetaskCallback(this.#deleteTask.bind(this));

        // tasklist.changestatusCallback(this.#updateTask.bind(this));
        console.log("before getTaskList");
        this.#getTaskList();


        //        const status = {
        //            "id": 1,
        //            "status": "DONE"
        //        };
        //        tasklist.updateTask(status);


        //        st.setStatuseslist(["WATING", "ACTIVE", "DONE"]);
        //        const myurl = `${config.servicesPath}/tasklist`
        //                console.log(myurl);


        //        const myTask = {
        //            "title": "cleaning",
        //            "status": "AKTIVE"
        //        };
        //        this.#addTask(myTask)


        //        const myurl = `${config.servicesPath}/tasklist`
        //        console.log(myurl);


    }

    #createLink() {
        const link = document.createElement('link');

        /**
         * Use directory of script as directory of CSS file
         * Observe, 'import.meta' is not yet part of the web standard.
         * At current, it is in stage 4 of the TC39 process.
         * See https://github.com/tc39/proposal-import-meta
         * All major current browseres do support import.meta
         **/
        const path = import.meta.url.match(/.*\//)[0];
        link.href = path.concat(this.#cssfile);
        link.rel = "stylesheet";
        link.type = "text/css";
        this.#shadow.appendChild(link);
    }

    #createHTML() {
        const wrapper = document.createElement('div');
        wrapper.id = "wrapper";

        const content = `
        <TASK-FORM></TASK-FORM>
        <VIEW-CONTENT></VIEW-CONTENT>
        `;

        wrapper.insertAdjacentHTML('beforeend', content);
        this.#shadow.appendChild(wrapper);

        return wrapper;
    }


    async #addTask(task) {
        const requestSettings = {
            "method": "POST",
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": JSON.stringify(task),
            "cache": "no-cache",
            "redirect": "error"
        };
        try {
            const response = await fetch(`../TaskServices/api/services/task`, requestSettings);
            if (response.ok) {
                const object = await response.json();
                console.log(object)
                if (typeof object.responseStatus != "undefined") {
                    if (object.responseStatus) {
                        const tasklist = this.#shadow.querySelector('task-list');
                        tasklist.showTask(object.task);
                    } else {
                        console.log("Could not connect to server");
                    }
                } else {
                    const object = await response.json();
                    console.log(object)
                    console.log("Could not connect to server");

                }
            }
        } catch (e) {
            console.log("Could not connect to server");
        }
    }


    async #getTaskList() {
        const url = `http://127.0.0.1:5000/getAllTasks`;
        try {
            const response = await fetch(url, {method: "GET", credentials: 'include'}); // Ensure cookies are sent
            if (response.ok) {
                const tasks = await response.json(); // Directly use the array of tasks
                console.log(tasks)
                const tasklist = this.#shadow.querySelector('view-content');
                if (tasks && Array.isArray(tasks)) { // Check if tasks is an array
                    tasks.forEach(task => {
                        tasklist.showTask(task); // Ensure showTask method is correctly defined
                    });
                } else {
                    console.log("No tasks found or incorrect data format.");
                }
            } else {
                console.error("Failed to fetch tasks: ", response.status);
            }
        } catch (e) {
            console.error("Could not connect to server", e);
        }
    }


    async #updateTask(taskStatus) {
        //        console.log(taskStatus);

        const requestSettings = {
            "method": "PUT",
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": JSON.stringify(taskStatus),
            "cache": "no-cache",
            "redirect": "error"
        };

        try {
            const response = await fetch(`../TaskServices/api/services/task/${taskStatus.id}`, requestSettings);
            if (response.ok) {
                const object = await response.json();
                if (typeof object.responseStatus != "undefined") {
                    if (object.responseStatus) {
                        const tasklist = this.#shadow.querySelector('task-list');
                        tasklist.updateTask(taskStatus)
                    } else {
                        console.log("Could not connect to server");
                    }
                } else {
                    console.log("Could not connect to server");
                }
            }
        } catch (e) {
            console.log("Could not connect to server");
        }
    }


    async #deleteTask(taskId) {
        const task = {
            "id": taskId
        };
        console.log("deleting: ")
        console.log(taskId)

        let requestSettings = {
            "method": "DELETE",
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "body": JSON.stringify(task),
            "cache": "no-cache",
            "redirect": "error",
            credentials: 'include'
        };

        try {

            const url = `http://127.0.0.1:5000/delete_task/${taskId}`;

            console.log(url);
            // const response = await fetch(url, {method: "GET", credentials: 'include'}); // Ensure cookies are sent


            const response = await fetch(url, requestSettings);
            if (response.ok) {
                const object = await response.json();
                if (typeof object.responseStatus != "undefined") {
                    if (object.responseStatus) {
                        const tasklist = this.#shadow.querySelector('task-list');
                        tasklist.removeTask(object.id);
                    } else {
                        console.log("Could not connect to server");
                    }
                } else {
                    console.log("Could not connect to server");
                }
            }
        } catch (e) {
            console.log("Could not connect to server");
        }
    }


}
