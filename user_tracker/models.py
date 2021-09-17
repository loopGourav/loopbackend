from django.db import models

# auth user model tables
from django.contrib.auth.models import User

from helper.models import StatusAbstractModel, DateAbstractModel
from helper.constants import VIDEO_CALL_STATUS


class VideoTracking(StatusAbstractModel):
    """
    VideoTracking
    Video Tracking models tables
    """
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='video_sender_video_tracker')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='video_receiver_video_tracker', null=True,
        blank=True)
    start_datetime = models.DateTimeField(
        verbose_name='Video Start Time', null=True, blank=True)
    end_datetime = models.DateTimeField(
        verbose_name='Video End Time', null=True, blank=True)
    time_duration = models.CharField(max_length=225,
                                     verbose_name='Time Duration',
                                     null=True, blank=True)
    video_call_status = models.CharField(
        max_length=100, choices=VIDEO_CALL_STATUS)

    class Meta:
        verbose_name = 'Video Tracking'
        verbose_name_plural = 'Video Tracking'
        db_table = 'video_tracking'

    def __str__(self):
        return str(self.sender.username)


class ChatTracking(StatusAbstractModel):
    """
    ChatTracking
    Chat Tracking models tables
    """
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='chat_sender_video_tracker')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='chat_receiver_video_tracker', null=True,
        blank=True)
    message = models.TextField(null=True, blank=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Chat Tracking'
        verbose_name_plural = 'Chat Tracking'
        db_table = 'chat_tracking'

    def __str__(self):
        return str(self.sender.username)


class BlockTracking(DateAbstractModel):
    """
    BlockTracking
    Block Tracking models tables
    """
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='block_sender_video_tracker')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='block_receiver_video_tracker', null=True,
        blank=True)
    is_block_status = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Block Tracking'
        verbose_name_plural = 'Block Tracking'
        db_table = 'block_tracking'

    def __str__(self):
        return str(self.sender.username)


class DeactivateUserCount(models.Model):
    """
    DeactivateUserCount
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='deactivate_user')
    count = models.IntegerField()

    class Meta:
        verbose_name = 'Deactivate User Count'
        verbose_name_plural = 'Deactivate User Count'
        db_table = 'deactivate_user_count'

    def __str__(self):
        return str(self.sender.username)


class UserEarning(models.Model):
    """
    UserEarning
    """
    earn_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='earn_user')
    spent_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='spent_user')
    amount = models.FloatField()
    video_call_tracking = models.ForeignKey(
        VideoTracking,
        on_delete=models.CASCADE,
        related_name='user_earn_video_tracking_instance')
    chat_tracking = models.ForeignKey(
        ChatTracking,
        on_delete=models.CASCADE,
        related_name='chat_tracking_instance')
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Earning User'
        verbose_name_plural = 'Earning User'
        db_table = 'earning_user'

    def __str__(self):
        return str(self.sender.username)


class UserVideoHistory(models.Model):
    """
    UserVideoHistory
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='video_history_user')
    video_call_tracking = models.ForeignKey(
        VideoTracking,
        on_delete=models.CASCADE,
        related_name='video_tracking_history_instance')

    class Meta:
        verbose_name = 'User Video History'
        verbose_name_plural = 'User Video History'
        db_table = 'user_video_history'

    def __str__(self):
        return str(self.sender.username)
