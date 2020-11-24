<script>
    $(document).ready(function() {
        blank = $("span[name='{{ q.blank_id }}']");
        blank.text("{{ q.blank_empty }}");
        $("#{{ q.key }}").on("input", function() {
            if ($(this).val() == ''){
                blank.text("{{ q.blank_empty }}");
            }
            else {
                blank.text($(this).val());
            }
        })
    })
</script>