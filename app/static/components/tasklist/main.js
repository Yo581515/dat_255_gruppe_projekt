//LIST
export default class extends HTMLElement {
    #shadow;
    #changeStatusCallback;
    #deleteCallback;
    #tbodyElm = null;
    #cssfile = "main.css";

    constructor() {
        // Always call super first in constructor
        super();

        // Entry point to the shadow DOM
        // If open, property "shadowRoot" will be an outside entrance to the shadow DOM
        this.#shadow = this.attachShadow({mode: 'closed'});
        this.#createLink();

        // Fetching the template element
        const task_list_Template = document.getElementById("task-list");
        // Copying the template content into a new document
        const task_list_Content = task_list_Template.content.cloneNode(true);
        this.#shadow.appendChild(task_list_Content);

        // Add a style element to shadow DOM that includes Bootstrap and custom styles
        //const style = document.createElement('style');
        style.textContent = `
        @import url('https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css');

        body {
            background-color: #212121;
            color: white;
        }
        table {
            display: block;
            width: 100%;
        }
        /* Include additional styles if necessary */
        `;

        // Append the style to the shadow DOM before appending the table
        //this.#shadow.appendChild(style);

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

    changestatusCallback(f) {
        this.#changeStatusCallback = f;
    }

    deletetaskCallback(f) {
        this.#deleteCallback = f;
    }


    //updates html
    updateTask(status) {
        const id = status.id;
        const newStatus = status.status;

        const taskELm = this.#shadow.querySelector(`tr[data-taskid="${id}"]`);
        //        console.log(taskELm);
        if (taskELm != null) {
            const oldStatusElm = taskELm.querySelector(`#status`);
            //            console.log(oldStatusElm);
            oldStatusElm.textContent = newStatus;

        }
    }

    //updates html
    noTask() {
        this.#tbodyElm = this.#shadow.querySelector("tbody");
        if (this.#tbodyElm == null || this.#tbodyElm.rows.length === 0) {
            const topMessage = document.querySelector('span[name="topMessage"]');
            topMessage.textContent = "No tasks were found";
        }
    }


    //updates html
    showTask(newtask) {
        // const topMessage = document.querySelector('span[name="topMessage"]');
        // topMessage.textContent = "";

        const id = newtask.id;
        const task_name = newtask.name;
        const task_description = newtask.description;
        console.log("tehee", id);
        console.log(newtask);

        this.#tbodyElm = this.#shadow.querySelector("tbody");

        if (this.#tbodyElm == null) {
            const wrapper = this.#shadow.getElementById("wrapper");

            const tableTemplate = document.getElementById("table-template");
            // Copying the template content into a new document
            const table = tableTemplate.content.cloneNode(true);

            wrapper.textContent = "";
            wrapper.appendChild(table);
            this.#shadow.appendChild(table);
            this.#tbodyElm = this.#shadow.querySelector("tbody");
        }

        const row = this.#tbodyElm.insertRow(-1);
        row.setAttribute("data-taskid", id);


        const erIdMed = 0;
        for (let i = 0; i < 5 - erIdMed; ++i) {
            row.insertCell(-1);
        }

        //        set erIdMed til 0 hvis du skall ha med id paa tabellen
        row.cells[erIdMed].id = id;
        row.cells[erIdMed].textContent = id;
        row.cells[erIdMed].style.verticalAlign = 'middle';


        const titelIndeks = 1 - erIdMed;
        row.cells[titelIndeks].id = "task_name";
        row.cells[titelIndeks].textContent = task_name;
        row.cells[titelIndeks].style.verticalAlign = 'middle';

        const statusIndeks = 2 - erIdMed;
        row.cells[statusIndeks].id = "task_description";
        row.cells[statusIndeks].textContent = task_description;


        // const selektorIndeks = 3 - erIdMed;

        //Create and append select list
        //const selectList = document.createElement("select");
        // const selectorId = id;
        // selectList.id = selectorId;
        //Create array of options to be added
        // const array = ["--Modify--", "ACTIVE", "WAITING", "DONE"];
        //        const i = 0;
        //Create and append the options
        // for (var i = 0; i < array.length; i++) {
        //    var option = document.createElement("option");
        //    if (array[i] === "--Modify--") {
        //        option.value = "";
        //    } else {
        //        option.value = array[i];
        //    }
        //    option.textContent = array[i];
        //    selectList.appendChild(option);
        //}
        // row.cells[selektorIndeks].id = "selector";
        //        eventLitsener for selectList
        /*selectList.addEventListener('change', (event) => {
            const denSelektorId = event.target.id;
            const denSelektorValue = event.target.value;
            const vidDuByStatusen = confirm(`set ${task_name} to ${denSelektorValue}?`);
            if (vidDuByStatusen && denSelektorValue !== "") {

                const nyStatus = {
                    "id": denSelektorId,
                    "status": denSelektorValue
                };

                this.#changestatus(nyStatus);
            } else {
                event.target.value = event.target.oldvalue;
            }
        });*/
        //row.cells[selektorIndeks].appendChild(selectList);
        //selectList.setAttribute("onfocus", "this.oldvalue = this.value;");
        //selectList.setAttribute("onchange", "this.oldvalue = this.value;");


        const deleteIndeks = 4 - erIdMed;
        const deleteId = id;
        row.cells[deleteIndeks].id = deleteId;
        const bt = document.createElement("button");
        bt.type = "button";
        bt.textContent = "Remove";
        bt.classList.add("btn", "btn-outline", "btn-success");
        //        eventLitsener for remove button
        bt.addEventListener("click", () => {
            const vilDusletteTasken = confirm(`delete task  '${task_name}'?`);
            if (vilDusletteTasken) {
                this.#deleteTask(deleteId)
                this.removeTask(deleteId);
            }
        });
        row.cells[deleteIndeks].appendChild(bt);
        row.cells[deleteIndeks].style.verticalAlign = 'middle';

    }


    #changestatus(id, newStatus) {
        this.#changeStatusCallback(id, newStatus);
    }

    #deleteTask(id) {
        this.#deleteCallback(id);
    }

    //updates html
    removeTask(id) {
        this.#tbodyElm = this.#shadow.querySelector('tbody');
        //        console.log(this.#tbodyElm);
        if (this.#tbodyElm != null) {
            const row = this.#tbodyElm.querySelector(`tr[data-taskid="${id}"]`);
            //            console.log(row);
            this.#tbodyElm.removeChild(row);

        }
        if (this.#tbodyElm != null && this.#tbodyElm.rows.length == 0) {
            const wrapper = this.#shadow.getElementById("wrapper");
            wrapper.textContent = "";
            this.#tbodyElm = null;
            this.noTask();
        }
    }

    //updates html
    setStatuseslist(optionList) {
        const array = optionList;
        this.#tbodyElm = this.#shadow.querySelector('tbody');
        if (this.#tbodyElm != null && this.#tbodyElm.rows.length !== 0) {
            const selectors = this.#tbodyElm.querySelectorAll('select');
            selectors.forEach((selectElm) => {
                //Create and append the options
                for (let i = 0; i < array.length; i++) {
                    const option = document.createElement("option");
                    if (array[i] === "--Modify--") {
                        option.value = "";
                    } else {
                        option.value = array[i];
                    }
                    option.textContent = array[i];
                    selectElm.appendChild(option);
                }
            });
        }
    }

}