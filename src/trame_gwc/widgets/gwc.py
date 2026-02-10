from trame_client.widgets.core import AbstractElement
from .. import module

__all__ = [
    "GirderAccessControl",
    "GirderAuthentication",
    "GirderBreadcrumb",
    "GirderDataBrowser",
    "GirderDataDetails",
    "GirderDataTable",
    "GirderFileManager",
    "GirderLogin",
    # "GirderJobList",
    "GirderProvider",
    "GirderRegister",
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
    :param has_permission: Boolean (default: False)Events
    :param forgot_password

    Events
    :param update_model_access
    :param update_has_permission
    :param close
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

        self._event_names += [
            ("update_model_access", "update:modelAccess"),
            ("update_has_permission", "update:hasPermission"),
            "close",
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

    Events
    :param forgot_password
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

        self._event_names += [
            ("forgot_password", "forgotPassword"),
        ]


class GirderBreadcrumb(HtmlElement):
    """
    Wraps GirderBreadcrumb Vue component

    :param location: Object (required)
    :param readonly: Boolean (default: False)
    :param append: Array (default: [])
    :param root_location_disabled: Boolean (default: False)

    Events
    :param crumb_click
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

        self._event_names += [
            ("crumb_click", "crumbClick"),
        ]


class GirderDataBrowser(HtmlElement):
    """
    Wraps GirderDataBrowser Vue component

    :param selected: Array (default [])
    :param location: Object (default null)
    :param root_location_disabled: Boolean (default False)
    :param selectable: Boolean (default False)
    :param draggable: Boolean (default False)
    :param options: Number (default { itemsPerPage: 10, page: 1 })

    Events
    :param update_selected
    :param update_location
    :param update_options
    :param row_click
    :param row_right_click
    :param drag
    :param drag_start
    :param drag_end
    :param drop
    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-data-browser",
            children,
            **kwargs,
        )

        self._attr_names += [
            "selected",
            "location",
            ("root_location_disabled", "rootLocationDisabled"),
            "selectable",
            "draggable",
            "options",
        ]

        self._event_names += [
            ("update_selected", "update:selected"),
            ("update_location", "update:location"),
            ("update_options", "update:options"),
            ("row_click", "rowClick"),
            ("row_right_click", "rowRightClick"),
            ("drag_start", "dragStart"),
            ("drag_end", "dragEnd"),
            "drag",
            "drop",
        ]


class GirderDataDetails(HtmlElement):
    """
    Wraps GirderDataDetails Vue component

    :param value: Array (required)
    :param info_keys: Array (default: DefaultInfoKeys)
    :param action_keys: Array (default: DefaultActionKeys)
    :param new_folder_enabled: Boolean (default False)

    Events
    :param action
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
            ("new_folder_enabled", "newFolderEnabled"),
        ]

        self._event_names += [
            "action",
        ]


class GirderDataTable(HtmlElement):
    """
    Wraps GirderDataTable Vue component

    :param draggable: Boolean (default False)
    :param loading: Bool (default False)
    :param options: Number (default { itemsPerPage: 10, page: 1 })
    :param rows: Array (default [])
    :param selectable: Boolean (default False)
    :param selected: Boolean Array (default [])
    :param server_items_length: Number (default 0)

    Events
    :param update_selected
    :param update_options
    :param row_click
    :param row_right_click
    :param drag
    :param drag_start
    :param drag_end
    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-data-table",
            children,
            **kwargs,
        )

        self._attr_names += [
            "selected",
            "location",
            ("root_location_disabled", "rootLocationDisabled"),
            "selectable",
            "draggable",
            "options",
        ]

        self._event_names += [
            ("update_selected", "update:selected"),
            ("update_options", "update:options"),
            ("row_click", "rowClick"),
            ("row_right_click", "rowRightClick"),
            ("drag_start", "dragStart"),
            ("drag_end", "dragEnd"),
            "drag",
        ]


class GirderFileManager(HtmlElement):
    """
    Wraps GirderFileManager Vue component

    :param selected: Array (default [])
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
    :param update_selected
    :param update_location
    :param update_options
    :param row_click
    :param row_right_click
    :param drag
    :param drag_start
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
            "selected",
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
            ("update_selected", "update:selected"),
            ("update_location", "update:location"),
            ("update_options", "update:options"),
            ("row_click", "rowClick"),
            ("row_right_click", "rowRightClick"),
            ("drag_start", "dragStart"),
            ("drag_end", "dragEnd"),
            "drag",
            "drop",
        ]


class GirderLogin(HtmlElement):
    """
    Wraps GirderLogin Vue component

    :param force_otp: Boolean (default: False)
    :param forgot_password_url: String (default: null)
    :param forgot_password_route: [Object, String] (default: null)
    :param hide_forgot_password: Boolean (default: False)
    :param oauth_providers: Boolean (default: False)

    Events
    :param forgot_password
    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-login",
            children,
            **kwargs,
        )

        self._attr_names += [
            ("force_otp", "forceOtp"),
            ("forgot_password_url", "forgotPasswordUrl"),
            ("forgot_password_route", "forgotPasswordRoute"),
            ("hide_forgot_password", "hideForgotPassword"),
            ("oauth_providers", "oauthProviders"),
        ]

        self._event_names += [
            ("forgot_password", "forgotPassword"),
        ]


# class GirderJobList(HtmlElement):
#     """
#     Wraps GirderJobList Vue component
#     """

#     def __init__(self, children=None, **kwargs):
#         super().__init__(
#             "girder-job-list",
#             children,
#             **kwargs,
#         )


class GirderProvider(HtmlElement):
    """
    Wraps GirderProvider Vue component

    Params:
    :compute_notification_bus: Boolean (default False)
    :listen_to_rest_client: Boolean (default True)  # NotificationBus param
    :use_event_source: Boolean (default False)  # NotificationBus param
    :with_credentials: Boolean (default False)  # NotificationBus param
    :api_root: String (default None)  # RestClient param
    :authenticate_with_credentials: Boolean (default False)  # RestClient param
    :use_girder_authorization_header: Boolean (default False)  # RestClient param
    :set_local_cookie: Boolean (default True)  # RestClient param

    Events
    :param user_logged_in
    :param user_logged_out
    :param user_registered
    :param api_root_updated
    :param user_fetched
    """

    _next_id = 0

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-provider",
            children,
            **kwargs,
        )

        self._attr_names = [
            ("compute_notification_bus", "computeNotificationBus"),
            ("listen_to_rest_client", "listenToRestClient"),
            ("use_event_source", "useEventSource"),
            ("with_credentials", "withCredentials"),
            ("api_root", "apiRoot"),
            ("authenticate_with_credentials", "authenticateWithCredentials"),
            ("use_girder_authorization_header", "useGirderAuthorizationHeader"),
            ("set_local_cookie", "setLocalCookie"),
        ]

        self._event_names += [
            ("user_logged_in", "userLoggedIn"),
            ("user_logged_out", "userLoggedOut"),
            ("user_registered", "userRegistered"),
            ("api_root_updated", "apiRootUpdated"),
            ("user_fetched", "userFetched"),
        ]

        GirderProvider._next_id += 1
        self._ref = kwargs.get("ref", f"GirderProvider_{GirderProvider._next_id}")
        self._attributes["ref"] = f'ref="{self._ref}"'

    def register_layout(self, layout):
        """
        Register self to the root of the layout and
        clear any previously registered elements (to support hot reloading)
        """
        self.clear()
        layout.root = self

    def logout(self):
        self.server.js_call(self._ref, "logout")

    def disconnect(self):
        self.server.js_call(self._ref, "setApiRoot", None)

    def connect(self, api_root):
        self.server.js_call(self._ref, "setApiRoot", api_root)

    def login(self, username, password, otp=None):
        self.server.js_call(self._ref, "login", username, password, otp)

    def fetch_user(self):
        self.server.js_call(self._ref, "fetchUser")


class GirderRegister(HtmlElement):
    """
    Wraps GirderRegister Vue component

    :param oauth_providers: Boolean (default: False)
    """

    def __init__(self, children=None, **kwargs):
        super().__init__(
            "girder-register",
            children,
            **kwargs,
        )

        self._attr_names += [
            ("oauth_providers", "oauthProviders"),
        ]


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
    :param update_search_mode
    :param update_search_types
    :param select
    :param error
    :param more_results
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
            ("update_search_mode", "update:searchMode"),
            ("update_search_types", "update:searchTypes"),
            "select",
            "error",
            "more_results",
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

    Events
    :param files_changed
    :param error
    :param done
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

        self._event_names += [
            ("files_changed", "filesChanged"),
            "error",
            "done",
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

        self._event_names += [
            "error",
            "dismiss",
            "done",
        ]
