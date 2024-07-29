/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.html"],
    theme: {
        extend: {
            fontFamily: {
                "source-code-pro": ["Source Code Pro", "monospace"]
            }
        },
    },
    plugins: [require('daisyui'),],
    daisyui: {
        themes: ["light", "dark", "cupcake", "retro"],
    },
    safelist: [
        'select',
        'select-bordered',
        "select-error",
        'input',
        'input-bordered',
        "input-error",
        'textarea',
        'textarea-bordered',
        "textarea-error",
        "alert",
        "alert-success",
        "alert-error",

    ]
}

