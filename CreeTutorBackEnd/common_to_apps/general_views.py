"""
File contains general view that could be adapted with use for any class.
"""

from django.shortcuts import render
from django.views import View

from common_to_apps.models import GeneralConfig, UserStatsForCharacterPerMinute, MediaAndSubtitleFiles


class IndexForListOfChoicesInSlidingWindow(View):
    """
    Renders and shows the list of choices in the db.
    """
    config_class = None
    user_stats_class = None
    media_table_to_filter_from = None
    template_to_render = None
    size_of_window_config = None
    min_number_of_choices_config = None

    def get_user_stats_or_defaults(self):
        """
        Method was created to get user's stats from the database. This class assumes the model is of type
        UserStatsForCharacterPerMinute or inherited from it. If this is not the case, the throws and error and
        forces the subclass to implement this method.
        :return:
        """
        raise NotImplementedError

    def get_list(self, min_window_filter, max_window_filter, min_number_of_choices, sliding_window_size):
        """
        Method returns the list of objects that should be rendered into the template
        :return:
        """
        raise NotImplementedError

    def get_sliding_window_size(self):
        """
        Goes to the config model and get the sliding window size for the activity
        :return:
        """
        # Check that the config file is related to general config, otherwise force the user to do this themselves
        if issubclass(self.config_class, GeneralConfig):
            return float(self.config_class.objects.get(name=self.size_of_window_config).config)
        else:
            raise TypeError("config_class does not inherit from GeneralConfig, implement this function for: "
                            + str(type(self.config_class)))

    def get_min_number_of_choices(self):
        """
        Goes to the config model and gets the minimum number of choices for this activity to be presented
        :return:
        """
        # Check that the config file is related to general config, otherwise force the user to do this themselves
        if issubclass(self.config_class, GeneralConfig):
            return float(self.config_class.objects.get(name=self.min_number_of_choices_config).config)
        else:
            raise TypeError("config_class does not inherit from GeneralConfig, implement this function for: "
                            + str(type(self.config_class)))

    def get_min_of_window(self, user_stat, sliding_window_size):
        """
        Method returns the lower end of the window that will be used to filter the choices.
        :return:
        """
        return user_stat - sliding_window_size

    def get_max_of_window(self, user_stat, sliding_window_size):
        """
        Method returns the upper end of the window that will be used to filter the choices.
        :return:
        """
        return user_stat + sliding_window_size

    def get(self, request):
        """
        Uses a sliding window to show choices that might be relevant to this user.
        :param request:
        :return:
        """
        if (
            self.config_class is None or
                self.user_stats_class is None or
                self.media_table_to_filter_from is None or
                self.template_to_render is None or
                self.size_of_window_config is None or
                self.min_number_of_choices_config is None
        ):
            raise ValueError("Set values for the "
                             "config_class, "
                             "user_stats_class, "
                             "media_table_to_filter_from, "
                             "template_to_render, "
                             "size_of_window_config, "
                             "min_number_of_choices_config "
                             "after inheriting this class.")

        sliding_window_size = self.get_sliding_window_size()
        min_number_of_choices = self.get_min_number_of_choices()

        # First we try to get the statistics of the user that is requested the page
        user_stat = self.get_user_stats_or_defaults()

        # Get the filter sizes
        min_window_filter = self.get_min_of_window(user_stat, sliding_window_size)
        max_window_filter = self.get_max_of_window(user_stat, sliding_window_size)

        # Now filtering the choices according to the window size and
        all_choices = self.get_list(min_window_filter, max_window_filter, min_number_of_choices, sliding_window_size)

        # Render the template
        context = {"all_choices": all_choices}

        return render(request, self.template_to_render, context)
