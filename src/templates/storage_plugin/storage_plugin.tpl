
%rebase("config/base.tpl", **locals())

<style>
td,th {
    padding: 5px;
}
.current {
    background-color: #00a2e2;
    color: white;
}
</style>

<div id="page-sample-plugin" class="config-page">
%include("_messages.tpl")

<form action="{{ request.fullpath }}" id="storage-form" method="post" class="config-form">
    <p>
    Here you can setup where your persistent data should be stored. If you want to use Nextcloud, LXC or other IO intensive applications, don't put them on internal flash, but always use external storage.
    </p>
    <p>Current device in use is {{ settings['old_device'].replace("/dev/","") }}</p>
    <input type="hidden" name="csrf_token" value="{{ get_csrf_token() }}">
    <input type="hidden" name="uuid" value="{{ settings['uuid'] }}">
    <input type="hidden" name="old_uuid" value="{{ settings['old_uuid'] }}">
    <input type="hidden" name="old_device" value="{{ settings['old_device'] }}">
    <table>
        <thead>
            <tr><th></th><th>{{ trans("Device") }}</th><th>{{ trans("Description") }}</th><th>{{ trans("Filesystem") }}</th><th>{{ trans("UUID") }}</th></tr>
        </thead>
        <tbody>
            %for drv in sorted(drives, key=lambda d: d['dev']):
                %if "/dev/{}".format(drv['dev']) == settings['old_device']:
            <tr class="current">
                %else:
            <tr>
                %end
                <td>
                    <input type="radio" name="new_disk" value="{{ drv['dev'] }}"/>
                </td>
                <td>{{ drv['dev'] }}</td>
                <td>{{ drv['description'] }}</td>
                <td>{{ drv['fs'] }}</td>
                <td>{{ drv['uuid'] }}</td>
            </tr>
            %end
        </tbody>
    </table>
    <br />
    <p>
    Changes to this setting will take effect on next reboot!
    </p>
    <button type="submit" name="send" class="button">{{ trans("Save") }}</button>
</form>

</div>

<script>
$(document).ready(function() {
    $("[name=new_disk]").val(["{{ settings['old_device'].replace("/dev/","") }}"]);
    %for drv in drives:
        %if 'uuid' in drv and drv['uuid'] == settings['uuid']:
    $("[name=new_disk]").val(["{{ drv['dev'] }}"]);
        %end
    %end
    $('#storage-form').submit(function() {
        var c = confirm("{{ trans("Are you sure you want to change where your srv is stored? Newly selected drive will be formated and you will loose all the data on it. Once formating is done, you'll get notification and you will be asked to reboot. On the reboot data will be moved from old drive to the new one. This can take some time so your next reboot will take longer. Are you sure you want to continue?") }}");
        return c;
    });
});
</script>
