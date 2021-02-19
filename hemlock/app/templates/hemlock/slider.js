<script>
    $(document).ready(function(){
        $("#{{ q.key }}").slider({
            formatter: function(value){
                {{ formatter }}
            }
        })
    })
</script>