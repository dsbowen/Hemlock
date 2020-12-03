<script>
    $(document).ready(function(){
        var input = $("#{{ q.key }}");
        var slider = $("#{{ q.key }}-slider");
        slider.val(input.val());
        input.on("input", function(){
            slider.val(input.val());
        });
        slider.on("input", function(){
            input.val(slider.val());
        });
    });
</script>