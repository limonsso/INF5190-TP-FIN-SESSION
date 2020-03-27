
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

