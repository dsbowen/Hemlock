<script>
    $(document).ready(function() {        
        function fill_blank() {
            if (question.val() == ''){
                blank.text("{{ q.blank_empty }}");
            }
            else {
                blank.text(question.val());
            }
        }

        question = $("#{{ q.key }}");
        blank = $("span[name='{{ q.blank_id }}']");
        fill_blank();
        question.on("input", function(){
            fill_blank();
        });
    })
</script>