from django.core.exceptions import ValidationError
from rest_framework import serializers


class BulkSerializerMixin:
    def __extract_pk_from_url(self, data, base_path):
        import re

        m = re.search(f"{base_path}([A-Za-z0-9]+)/", data)
        if m:
            found = m.group(1)
            return found

    def to_internal_value(self, data):
        ret = super(BulkSerializerMixin, self).to_internal_value(data)

        id_attr = getattr(self.Meta, "update_lookup_field", "pk")
        lookup_field_type = getattr(self.Meta, "lookup_field_type", int)

        request_method = getattr(
            getattr(self.context.get("view"), "request"), "method", ""
        )
        request_path = getattr(getattr(self.context.get("view"), "request"), "path", "")

        # add update_lookup_field field back to validated data
        # since super by default strips out read-only fields
        # hence id will no longer be present in validated_data
        if all(
            (
                isinstance(self.root, BulkListSerializer),
                id_attr,
                request_method in ("PUT", "PATCH"),
            )
        ):
            id_field = self.fields[id_attr]
            id_value = id_field.get_value(data)

            if type(id_field) == serializers.HyperlinkedIdentityField:
                # Give the test restrictions this dirty regex match is required to extract  the id
                db_id_val = self.__extract_pk_from_url(
                    data=id_value, base_path=request_path
                )
                # Added this hack to cast the model ID to the right value.
                ret[id_field.lookup_field] = lookup_field_type(db_id_val)
            ret[id_attr] = id_value

        return ret


class BulkListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        # Maps for id->instance and id->data item.
        # Retrieve the id field we are using to extract filter records, for the example is url
        # since we are using HyperlinkedIdentityField fields given the test restrictions
        id_attr = getattr(self.child.Meta, "update_lookup_field", "pk")
        id_field = self.child.fields[id_attr]
        obj_mapping = {obj.id: obj for obj in instance}
        # Get the lookup_field (default pk) defined for the HyperlinkedIdentityField
        data_mapping = {item[id_field.lookup_field]: item for item in validated_data}

        # Perform creations and updates.
        ret = []
        for obj_id, data in data_mapping.items():
            obj = obj_mapping.get(obj_id, None)
            if obj is None:
                raise ValidationError(f"Record with id {obj_id} does not exist.")
            else:
                record = self.child.update(obj, data)
                ret.append(record)

        return ret
