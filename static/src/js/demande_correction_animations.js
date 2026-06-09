/** @odoo-module **/

const FORM_SELECTOR = ".o_form_view.ar_demande_correction_form";
function animateForm(form) {
    if (!form || form.dataset.arDcAnimated === "1") {
        return;
    }
    form.dataset.arDcAnimated = "1";

    const sheet = form.querySelector(".ar_sortie_caisse_sheet");
    if (sheet) {
        sheet.classList.add("ar_sc_ready");
    }

    form.querySelectorAll(".ar_sortie_caisse_title, .ar_sortie_caisse_panel").forEach((element) => {
        element.classList.add("ar_sc_reveal");
    });
}

function scan() {
    document.querySelectorAll(FORM_SELECTOR).forEach(animateForm);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
} else {
    scan();
}

if (document.body) {
    const bodyObserver = new MutationObserver(scan);
    bodyObserver.observe(document.body, {
        childList: true,
        subtree: true,
    });
}
