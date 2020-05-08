"""
File contains general view that have been specialized for activities that use characters per minute as the main
statistic. For now, this only includes shadowing and transcription
"""
from django.db.models import Min

from common_to_apps.general_views import IndexForListOfChoicesInSlidingWindow
from common_to_apps.models import UserStatsForCharacterPerMinute, MediaAndSubtitleFiles


class IndexForListOfChoicesInWindowForUserStatsForCharacterPerMinuteOrSubclasses(IndexForListOfChoicesInSlidingWindow):
    """
    Subclasses IndexForListOfChoicesInWindow. This is done to reduce the amount of code duplication by implementing
    methods that will fetch stats from UserStatsForCharacterPerMinutes' subclasses.
    """
    def get_user_stats_or_defaults(self):
        """
        Method was created to get user's stats from the database. This class assumes the model is inherited from
        UserStatsForCharacterPerMinute and MediaAndSubtitleFiles. If this is not the case, the throws an error and
        forces the subclass to implement this method.
        :return:
        """
        if issubclass(self.user_stats_class, UserStatsForCharacterPerMinute) and \
                issubclass(self.media_table_to_filter_from, MediaAndSubtitleFiles):
            # Get the user stats, if they don't exist, get default
            try:
                user_stats = self.user_stats_class.objects.get(user_id=self.request.user.id)
            except self.user_stats_class.DoesNotExist:
                user_stats = self.user_stats_class(
                    user=self.request.user,
                    chars_per_minute=self.media_table_to_filter_from.objects.aggregate(
                        Min('chars_per_minute'))['chars_per_minute__min']
                )

                user_stats.save()

            return user_stats.chars_per_minute
        else:
            raise TypeError("user_stats_class does not inherit from UserStatsForCharacterPerMinute or "
                            "media_table_to_filter_from does not inherit from MediaAndSubtitleFiles"
                            ", implement this function for: "
                            + str(type(self.user_stats_class)) + " and " + str(type(self.media_table_to_filter_from)))

    def get_list(self, min_window_filter, max_window_filter, min_number_of_choices, sliding_window_size):
        """
        Method returns the list of objects that should be rendered into the template. This class assumes the model is
        inherited from MediaAndSubtitleFiles. If this is not the case, the throws an error and forces the subclass to
        implement this method.
        :return:
        """
        if issubclass(self.media_table_to_filter_from, MediaAndSubtitleFiles):
            all_choices = []
            # Get the choices, expand the window size if not enough found
            while len(all_choices) < min_number_of_choices:
                all_choices = self.media_table_to_filter_from.objects.filter(
                    chars_per_minute__range=(min_window_filter, max_window_filter)
                )

                min_window_filter -= sliding_window_size
                max_window_filter += sliding_window_size
            return all_choices
        else:
            raise TypeError("config_class does not inherit from GeneralConfig, implement this function for: "
                            + str(type(self.media_table_to_filter_from)))
