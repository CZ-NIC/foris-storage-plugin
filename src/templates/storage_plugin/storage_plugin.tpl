
%rebase("config/base.tpl", **locals())

<style>
td,th {
    padding: 5px;
}
th {
    font-weight: bold;
}
tbody tr:hover {
    background-color: #f2f2f2;
}
</style>

<div id="page-sample-plugin" class="config-page">
%include("_messages.tpl")

<form action="{{ request.fullpath }}" id="storage-form" method="post" class="config-form">
    <p>
    {{ trans("Here you can setup where your persistent data should be stored. If you want to use Nextcloud, LXC or other IO intensive applications, don't put them on internal flash, but always use external storage. Also make sure that your data will fit on the new drive before switching.") }}
    </p>
    <p>
    {{! trans("Once you choose a drive, it will be formatted to Btrfs filesystem and on next reboot your <em>/srv</em> (directory where all IO intesive applications should reisde) will get moved to this new drive.") }}
    </p>
    </p>
    <span id="test-results">
    <p class="{{! settings['old_uuid'] == 'rootfs' and 'result test-fail' or 'result test-success' }}">
    {{ trans("Device currently in use is {} ({}).").format(settings['old_device'].replace("/dev/",""), settings['old_uuid'] == 'rootfs' and 'internal flash' or 'uuid: {}'.format(settings['old_uuid'])) }}
    </p>
    </span>
    %if settings['formating']:
    <p>
    {{ trans("Processing changes at the moment, please wait...") }}
    </p>
    %end
    %if drives:
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
            <tr class="button" style="display: table-row; height: 1em; line-height: 1em;">
                %else:
            <tr onClick='$("input[name=new_disk]").val(["{{ drv['dev']  }}"]).change();'>
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
    {{ trans("Changes to this setting will take effect on next reboot!") }}
    </p>
    <button type="submit" name="send" class="button">{{ trans("Format & Set") }}</button>
    %else:
    <p>{{ trans("No drives connected, please connect a drive and refresh the page.") }}</p>
    %end
</form>

</div>

<script>
$(document).ready(function() {
    $("[name=new_disk]").val(["{{ settings['old_device'].replace("/dev/","") }}"]);
    %for drv in drives:
        %if 'uuid' in drv and drv['uuid'] == settings['uuid'] and settings['uuid']:
    $("[name=new_disk]").val(["{{ drv['dev'] }}"]);
        %end
    %end
    $("[name=send]").prop('disabled', true);
    $("[name=new_disk]").change(function() { $("[name=send]").prop('disabled', false); });
    %if settings['formating']:
    $("[name=new_disk]").prop('disabled', true);
    setInterval(function() { location.reload(); }, 10000);
    %end
    $('#storage-form').submit(function() {
        var c = confirm("{{! trans("Are you sure you want to change where your srv is stored? Newly selected drive will be formated and you will loose all the data on it. Once formating is done, you'll get notification and you will be asked to reboot. On the reboot data will be moved from old drive to the new one. This can take some time so your next reboot will take longer. Are you sure you want to continue?") }}");
        return c;
    });
});
</script>
