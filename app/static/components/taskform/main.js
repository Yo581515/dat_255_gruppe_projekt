//FORM
export default class extends HTMLElement {
    #shadow;
    #newTaskCallback;
    constructor() {
        // Always call super first in constructor
        super();

        // Entry point to the shadow DOM
        // If open, property "shadowRoot" will be an outside entrance to the shadow DOM
        this.#shadow = this.attachShadow({ mode: 'closed' });


        // Fetching the template element
        const task_form_Template = document.getElementById("task-form");
        // Copying the template content into a new document
        const task_form_Content = task_form_Template.content.cloneNode(true);
        this.#shadow.appendChild(task_form_Content);

        const bt = this.#shadow.querySelector('button[type=button]');


        bt.addEventListener('click', this.#showDialogForm.bind(this));
        const form = this.#shadow.querySelector('form');
        form.addEventListener('submit', this.#send.bind(this));

    }



    //updates html
    enableaddtask() {
        const bt = this.#shadow.querySelector('button[type=button]');
        bt.disabled = false;
        const topMessage = document.querySelector('span[name="topMessage"]');
        topMessage.textContent = "button enabled";
    }


    addtaskCallback(f) {
        this.#newTaskCallback = f;
    }


    #showDialogForm() {
        const dialog = this.#shadow.querySelector('#modal');
        dialog.show();
    }

    #send(event) {

        event.preventDefault();

        const dialog = this.#shadow.querySelector('#modal');
        dialog.close();

        const topMessage = document.querySelector('span[name="topMessage"]');
        topMessage.textContent = "";

        const task = {};
        const taskData = new FormData(event.target);
        for (let pair of taskData) {
            task[pair[0]] = pair[1].trim();
        }

//        console.log(task);

        this.#newTaskCallback(task);

    }



}