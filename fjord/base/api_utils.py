from django.conf import settings

import pytz
from rest_framework import fields
from rest_framework import serializers


class UTCDateTimeField(fields.DateTimeField):
    """Like DateTimeField, except it is always in UTC in the API"""
    def to_native(self, value):
        """Convert outgoing datetimes into UTC

        Input currently saves everything in Pacific time, so this
        takes the datetimes and converts them from Pacific time to
        UTC.

        If this situation ever changes, then we'd change
        settings.TIME_ZONE and this should continue to work.

        """
        if value is not None and value.tzinfo is None:
            default_tzinfo = pytz.timezone(settings.TIME_ZONE)
            value = default_tzinfo.localize(value)
            value = value.astimezone(pytz.utc)
        return super(UTCDateTimeField, self).to_native(value)

    def from_native(self, value):
        """Converts incoming strings to localtime

        Input currently saves everything in Pacific time, so this
        takes the datetime that super().from_native() produces,
        converts it to localtime and if USE_TZ=False, drops the timezone.

        If this situation ever changes, this should continue to work.

        """
        result = super(UTCDateTimeField, self).from_native(value)

        if result is not None and result.tzinfo is not None:
            # Convert from whatever timezone it's in to local
            # time.
            local_tzinfo = pytz.timezone(settings.TIME_ZONE)
            result = result.astimezone(local_tzinfo)

            # If USE_TZ = False, drop the timezone
            if not settings.USE_TZ:
                result = result.replace(tzinfo=None)
        return result


class StrictArgumentsMixin(object):
    """DRF Serializer mixin that requires init_data to be a subset of
    fields

    This is for API endpoints that require that all arguments passed in
    are handled. If an argument is specified that doesn't exist, then
    this will raise a ``serializers.ValidationError`` during validation.

    To use::

        from rest_framework import serializers

        from fjord.base.api_utils import StrictArgumentsMixin


        class MySerializer(StrictArgumentMixin, serializers.Serializer):
            ...

    """
    def validate(self, data):
        data = super(StrictArgumentsMixin, self).validate(data)

        # Guarantee that arguments passed in are a subset of possible
        # fields.
        if self.init_data:
            for key in self.init_data.keys():
                if key not in self.fields:
                    raise serializers.ValidationError(
                        '"{0}" is not a valid argument.'.format(key)
                    )

        return data
