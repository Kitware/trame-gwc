from trame_client.widgets.core import AbstractElement
from .. import module

__all__ = [
    "GirderAccessControl",
    "GirderAuthentication",
    "GirderBreadcrumb",
    "GirderDataDetails",
    "GirderFileManager",
    "GirderJobList",
    "GirderProvider",
    "GirderSearch",
    "GirderUpload",
    "GirderUpsertFolder",
]


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


class GirderAccessControl(HtmlElement):
    """
    Wraps GirderAccessControl Vue component

    :param model: Object (required)
    :param has_permission: Boolean (default: False)

    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-access-control",
            children,
            **kwargs,
        )

        self._attr_names += [
            "model",
            ("has_permission", "hasPermission"),
        ]


class GirderAuthentication(HtmlElement):
    """
    Wraps GirderAuthentication Vue component

    :param register: Boolean (default: False)
    :param oauth: Boolean (default: False)
    :param forgot_password_url: String (default: null)
    :param forgot_password_route: [Object, String] (default: null)
    :param force_otp: Boolean (default: False)
    :param hide_forgot_password: Boolean (default: False)

    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-authentication",
            children,
            **kwargs,
        )

        self._attr_names += [
            "register",
            "oauth",
            ("forgot_password_url", "forgotPasswordUrl"),
            ("forgot_password_route", "forgotPasswordRoute"),
            ("force_otp", "forceOtp"),
            ("hide_forgot_password", "hideForgotPassword"),
        ]


class GirderBreadcrumb(HtmlElement):
    """
    Wraps GirderBreadcrumb Vue component

    :param location: Object (required)
    :param readonly: Boolean (default: False)
    :param append: Array (default: [])
    :param root_location_disabled: Boolean (default: False)
    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-breadcrumb",
            children,
            **kwargs,
        )

        self._attr_names += [
            "location",
            "readonly",
            "append",
            ("root_location_disabled", "rootLocationDisabled"),
        ]


class GirderDataDetails(HtmlElement):
    """
    Wraps GirderDataDetails Vue component

    :param value: Array (required)
    :param info_keys: Array (default: DefaultInfoKeys)
    :param action_keys: Array (default: DefaultActionKeys)
    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-data-details",
            children,
            **kwargs,
        )

        self._attr_names += [
            ("value", "value"),
            ("info_keys", "infoKeys"),
            ("action_keys", "actionKeys"),
        ]

        self._event_names += [
            "action",
        ]


class GirderFileManager(HtmlElement):
    """
    Wraps GirderFileManager Vue component

    :param value: Array (default [])
    :param location: Object (default null)
    :param root_location_disabled: Boolean (default False)
    :param no_access_control: Boolean (default False)
    :param selectable: Boolean (default False)
    :param drag_enabled: Boolean (default False)
    :param upload_enabled: Boolean (default False)
    :param new_folder_enabled: Boolean (default False)
    :param upload_max_show: Number (default 0)
    :param upload_multiple: Boolean (default False)
    :param upload_accept: String (default '*')
    :param pre_upload: Function (default: async {})
    :param post_upload: Function (default: async {})
    :param pre_upsert: Function (default: async {})
    :param post_upsert: Function (default: async {})
    :param items_per_page: Number (default 10)
    :param items_per_page_options: Array (default [10, 25, 50])

    Events

    :param update_location
    :param update_items_per_page
    :param input
    :param selection_changed
    :param rowclick
    :param drag
    :param dragstart
    :param dragend
    :param drop

    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-file-manager",
            children,
            **kwargs,
        )

        self._attr_names += [
            "value",
            "location",
            ("root_location_disabled", "rootLocationDisabled"),
            ("no_access_control", "noAccessControl"),
            "selectable",
            ("drag_enabled", "dragEnabled"),
            ("upload_enabled", "uploadEnabled"),
            ("new_folder_enabled", "newFolderEnabled"),
            ("upload_max_show", "uploadMaxShow"),
            ("upload_multiple", "uploadMultiple"),
            ("upload_accept", "uploadAccept"),
            ("preUpload", "preUpload"),
            ("post_upload", "postUpload"),
            ("pre_upsert", "preUpsert"),
            ("post_upsert", "postUpsert"),
            ("items_per_page", "itemsPerPage"),
            ("items_per_page_options", "itemsPerPageOptions"),
        ]

        self._event_names += [
            ("update_location", "update:location"),
            ("update_items_per_page", "update:itemsPerPage"),
            "input",
            ("selection_changed", "selection-changed"),
            "rowclick",
            "drag",
            "dragstart",
            "dragend",
            "drop",
        ]


class GirderJobList(HtmlElement):
    """
    Wraps GirderJobList Vue component

    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-job-list",
            children,
            **kwargs,
        )


class GirderProvider(HtmlElement):
    """
    Wraps GirderProvider Vue component

    :param value: String (required)

    """

    _next_id = 0

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-rest-provider",
            children,
            **kwargs,
        )

        self._attr_names = [
            "value",
        ]

        GirderProvider._next_id += 1
        self._ref = kwargs.get("ref", f"GirderProvider_{GirderProvider._next_id}")
        self._attributes["ref"] = f'ref="{self._ref}"'

    def logout(self):
        self.server.js_call(self._ref, "logout")

    def register_layout(self, layout):
        """
        Register self to the root of the layout and
        clear any previously registered elements (to support hot reloading)
        """
        self.clear()
        layout.root = self


class GirderSearch(HtmlElement):
    """
    Wraps GirderSearch Vue component

    :param hide_search_icon: Boolean (default: False)
    :param hide_options_menu: Boolean (default: False)
    :param max_quick_results: Number (default: 6)
    :param placeholder: String (default: null)
    :param search_mode_options: Array (default: SearchModeOptions)
    :param search_mode: String (default: null)
    :param search_type_options: Array (default: SearchTypeOptions)
    :param search_types: validator (default: null)
    :param show_more: Boolean (default: False)

    Events

    :param select

    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-search",
            children,
            **kwargs,
        )

        self._attr_names += [
            ("hide_search_icon", "hideSearchIcon"),
            ("hide_options_menu", "hideOptionsMenu"),
            ("max_quick_results", "maxQuickResults"),
            "placeholder",
            ("search_mode_options", "searchModeOptions"),
            ("search_mode", "searchMode"),
            ("search_type_options", "searchTypesOptions"),
            ("search_type", "searchTypes"),
            ("show_more", "showMore"),
        ]

        self._event_names += [
            "select",
        ]


class GirderUpload(HtmlElement):
    """
    Wraps GirderUpload Vue component

    :param dest: Object (required)
    :param max_show: Number (default: 0)
    :param multiple: Boolean (default: True)
    :param pre_upload: Function (default: {})
    :param post_upload: Function (default: {})
    :param upload_cls: Function (default: Upload)
    :param accept: Object (required)
    :param start_button_text: String (default: 'Start Upload')
    :param hide_start_button: Boolean (default: False)
    :param hide_headline: Boolean (default: False)

    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-upload",
            children,
            **kwargs,
        )

        self._attr_names += [
            "dest",
            ("max_show", "maxShow"),
            "multiple",
            ("pre_upload", "preUpload"),
            ("post_upload", "postUpload"),
            ("upload_cls", "uploadCls"),
            "accept",
            ("start_button_text", "startButtonText"),
            ("hide_start_button", "hideStartButton"),
            ("hide_headline", "hideHeadline"),
        ]


class GirderUpsertFolder(HtmlElement):
    """
    Wraps GirderUpsertFolder Vue component

    :param location: Object (required)
    :param edit: Boolean (default: False)
    :param pre_upsert: Function (default: {})
    :param post_upsert: Function (default: {})

    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-upsert-folder",
            children,
            **kwargs,
        )

        self._attr_names += [
            "location",
            "edit",
            ("pre_upsert", "preUpsert"),
            ("post_upsert", "postUpsert"),
        ]
