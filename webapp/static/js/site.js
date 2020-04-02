$('#quick-search-submit').click(function (e) {
    e.preventDefault();
    var date_du = $('#date_du');
    var date_au = $('#date_au');
    if (date_du.val() === '') {
        date_du.addClass('is-invalid')
        return;
    } else {
        if (date_du.hasClass('is-invalid'))
            date_du.removeClass('is-invalid')
    }
    if (date_au.val() === '') {
        date_au.addClass('is-invalid')
        return;
    } else {
        if (date_au.hasClass('is-invalid'))
            date_au.removeClass('is-invalid')
    }
    var alert_qck_search = $('#alert-error-qck-search')
    if (date_du.val() > $('#date_au').val()) {
        alert_qck_search.removeClass('hidden')
    } else {
        if (!alert_qck_search.hasClass('hidden')) {
            alert_qck_search.addClass('hidden')
            return;
        }
    }

    fetch(`${window.location.origin}/contrevenants?du=${date_du.val()}&au=${date_au.val()}`)
        .then(function (data) {
            data.json().then(function (response) {
                $('#quick-search-result tbody').empty();
                let group = response.reduce((r, a) => {
                    r[a.etablissement] = [...r[a.etablissement] || [], a];
                    return r;
                }, {});
                var html = '';
                Object.keys(group).forEach((elt, index) => {
                    html += `<tr>
                                <td scope="row">${elt}</td>
                                <th scope="row">${group[elt].length} contravention${group[elt].length > 1 ? 's' : ''}</th>                          
                            </tr>`
                });
                $('#quick-search-result tbody:last-child').append(html);

                getPagination('#quick-search-result');
            });
        })
        .catch(function (error) {
            console.log(error)
        });
});

$('#edit_contrevenant').on('show.bs.modal', function (e) {
    var contrevenant = e.relatedTarget.dataset;
    console.log(contrevenant);
    $('#contrevenant-id').val(contrevenant.id)
    $('#contrevenant-proprietaire').val(contrevenant.proprietaire)
    $('#contrevenant-etablissement').append(contrevenant.etablissement)
    $('#contrevenant-description').val(contrevenant.description)
    $('#contrevenant-date-jugement').val(contrevenant.date_jugement)
    $('#contrevenant-date-infraction').val(contrevenant.date_infraction)
    $('#contrevenant-montant').val(contrevenant.montant.split(' ')[0])
});

$('#edit_contrevenant').on('hide.bs.modal', function (e) {
    location.reload();
});

$('#btnUpdateContrevenant').click(function (e) {
    $('.contrevenantEditionForm').submit();
});

$(document).ready(function () {
    $('.contrevenantEditionForm').bootstrapValidator({
        fields: {
            contrevenant_description: {
                validators: {
                    notEmpty: {
                        message: "La description de contrevenant est réquis et ne peut être vide"
                    }
                }
            },
            contrevenant_date_jugement: {
                validators: {
                    date: {
                        format: 'MM/DD/YYYY',
                        message: "L'entrée n'est pas valide"
                    },
                    callback: {
                        message: "La date de jugement doit être superieure à la date d'infraction",
                        callback: function (value, validator, $field) {
                            return $('#contrevenant-date-infraction').val() < value
                        }
                    }
                }
            },
            contrevenant_montant: {
                validators: {
                    greaterThan: {
                        inclusive: false,
                        value: 0,
                        message: "Le montant doit être superieur a zéro"
                    }
                }
            }
        }
    }).on('success.form.bv', function (e) {
        // Prevent form submission
        e.preventDefault();

        var data = {
            id: $('#contrevenant-id').val(),
            description: $('#contrevenant-description').val(),
            date_jugement: $('#contrevenant-date-jugement').val(),
            montant: $('#contrevenant-montant').val()
        }
        update_contrevenant(data);
    });
});

function delete_contrevenant(id) {
    Swal.fire({
        title: 'Suppression de contrevenant!',
        text: 'Voulez-vous vraiment supprimer ce contrevenant ?',
        icon: 'warning',
        showCancelButton: true,
        cancelButtonText: 'Non',
        confirmButtonText: 'Oui',
        preConfirm: function () {
            return fetch(`${window.location.origin}/contrevenants/${id}`, {method: 'DELETE'})
                .then(response => {
                    console.log(response)
                    if (!response.ok) {
                        throw new Error(response.statusText)
                    }
                    Swal.fire({
                        title: 'Suppression de contravention!',
                        text: 'La contravention a été supprimée avec succès',
                        icon: 'success',
                        preConfirm: function () {
                            location.reload();
                        }
                    })
                })
                .catch(error => {
                    Swal.showValidationMessage(
                        `Request failed: ${error}`
                    )
                })
        }
    })
}

function update_contrevenant(data) {
    console.log(data);

    fetch(`${window.location.origin}/contrevenants/${data.id}`,
        {
            method: 'PATCH',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then((response) => {
            console.log(response.json());
            //return response.json();
            var Toast = Swal.mixin({
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 2000,
                timerProgressBar: true,
                onOpen: (toast) => {
                    toast.addEventListener('mouseenter', Swal.stopTimer)
                    toast.addEventListener('mouseleave', Swal.resumeTimer)
                },
                onClose: () => {
                    location.reload();
                }
            });
            if (!response.ok) {
                Toast.fire({
                    icon: 'error',
                    title: 'Signed in successfully'
                });
            } else
                Toast.fire({
                    icon: 'success',
                    title: 'Signed in successfully'
                });
        })
        .then((data) => {
            console.log(data);
        });


}