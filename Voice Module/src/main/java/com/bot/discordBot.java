package com.bot;

import com.sedmelluq.discord.lavaplayer.player.AudioPlayerManager;
import com.sedmelluq.discord.lavaplayer.player.DefaultAudioPlayerManager;
import com.sedmelluq.discord.lavaplayer.source.AudioSourceManagers;
import net.dv8tion.jda.core.AccountType;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.JDA;
import net.dv8tion.jda.core.JDABuilder;
import net.dv8tion.jda.core.entities.Member;
import net.dv8tion.jda.core.events.guild.voice.GuildVoiceLeaveEvent;
import net.dv8tion.jda.core.events.guild.voice.GuildVoiceMoveEvent;
import net.dv8tion.jda.core.hooks.ListenerAdapter;
import com.sedmelluq.discord.lavaplayer.player.AudioLoadResultHandler;
import com.sedmelluq.discord.lavaplayer.tools.FriendlyException;
import com.sedmelluq.discord.lavaplayer.track.AudioPlaylist;
import com.sedmelluq.discord.lavaplayer.track.AudioTrack;
import net.dv8tion.jda.core.entities.Guild;
import net.dv8tion.jda.core.entities.TextChannel;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;
import net.dv8tion.jda.core.managers.AudioManager;

/**
 * Created by Jess Walter on 3/28/2017.
 */

import java.util.HashMap;
import java.util.Map;

public class discordBot extends ListenerAdapter {
    private static String nickName;
    private static String avatarURL;

    public static void main(String[] args) throws Exception {
        Config config = new Config();
        JDA jda = new JDABuilder(AccountType.BOT)
                .setToken(config.getToken("Discord"))
                .buildBlocking();

        jda.addEventListener(new discordBot());
        nickName = jda.getSelfUser().getName();
        avatarURL = jda.getSelfUser().getAvatarUrl();
    }

    private final AudioPlayerManager playerManager;
    private final HashMap<Long, ServerMusicManager> musicManagers;


    private discordBot() {
        this.musicManagers = new HashMap<>();

        this.playerManager = new DefaultAudioPlayerManager();
        AudioSourceManagers.registerRemoteSources(playerManager);
        AudioSourceManagers.registerLocalSource(playerManager);
    }

    private synchronized ServerMusicManager getServerAudioPlayer(Guild guild) {
        long guildId = Long.parseLong(guild.getId());
        ServerMusicManager musicManager = musicManagers.get(guildId);

        if (musicManager == null) {
            musicManager = new ServerMusicManager(playerManager);
            musicManagers.put(guildId, musicManager);
        }

        guild.getAudioManager().setSendingHandler(musicManager.getSendHandler());

        return musicManager;
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        String[] command = event.getMessage().getContent().split(" ", 2);
        Guild guild = event.getGuild();

        if (guild != null) {
            if ("~play".equals(command[0]) && command.length == 2) {
                if (event.getMember().getVoiceState().getChannel() == null) {
                    event.getTextChannel().sendMessage("You are not connected to a voice channel :cry:").queue();
                    return;
                }
                loadAndPlay(event.getTextChannel(), command[1], event.getMember());
            } else if ("~skip".equals(command[0])) {
                skipTrack(event.getTextChannel());
            } else if ("~playlist".equals(command[0])) {
                getPlaylist(event.getTextChannel());
            } else if ("~stop".equals(command[0])) {
                stopPlayer(event.getTextChannel());
            } else if ("~pause".equals(command[0])) {
                pauseTrack(event.getTextChannel());
            } else if ("~resume".equals(command[0])) {
                resumeTrack(event.getTextChannel());
            } else if ("~voicestats".equals(command[0])) {
                voiceStats(event.getTextChannel());
            } else if ("~search".equals(command[0])) {
                //search(event.getTextChannel(), command[1], event.getMember());
                //event.getTextChannel().sendMessage("Search functionality coming soon. Checkout the discord server for frequent updates.").queue();
            }
        }

        super.onMessageReceived(event);
    }

    @Override
    public void onGuildVoiceLeave(GuildVoiceLeaveEvent event) {
        checkVoiceLobby(event.getGuild());
    }

    @Override
    public void onGuildVoiceMove(GuildVoiceMoveEvent event) {
        checkVoiceLobby(event.getGuild());
    }

    private void loadAndPlay(final TextChannel channel, final String trackUrl, final Member author) {
        final ServerMusicManager musicManager = getServerAudioPlayer(channel.getGuild());
        String url = trackUrl.split(" ")[0];
        channel.sendTyping().queue();

        playerManager.loadItemOrdered(musicManager, url, new AudioLoadResultHandler() {
            @Override
            public void trackLoaded(AudioTrack track) {
                channel.sendMessage("Adding to queue " + track.getInfo().title).queue();

                play(channel.getGuild(), musicManager, track, author);
            }

            @Override
            public void playlistLoaded(AudioPlaylist playlist) {

                if (trackUrl.split(" ").length == 1) {
                    channel.sendMessage("Playlist detected. Please try again but include the songs you want included.\n" +
                            "Example: `~play *playlist url* 1-5` This would load songs 1-5 on the playlist. Limited to loading up to 10 songs at a time.").queue();
                } else {
                    String songs = trackUrl.split(" ")[1];
                    if (songs.split("-").length == 2) {
                        int to, from;
                        try {
                            from = Integer.parseInt(songs.split("-")[0]);
                            to = Integer.parseInt(songs.split("-")[1]);
                        } catch (NumberFormatException e) {
                            channel.sendMessage(":x: NumberFormatException: Invalid number given, please only user numeric characters :x:").queue();
                            return;
                        }
                        if (from > to) {
                            channel.sendMessage(":x: Error: Beginning index is bigger than ending index :x:").queue();
                            return;
                        } else if (to > playlist.getTracks().size()) {
                            channel.sendMessage(":x: Error: Requesting tracks out of range. Only " + playlist.getTracks().size() + " tracks in playlist :x:").queue();
                            return;
                        } else if (to - from > 9) {
                            channel.sendMessage(":exclamation: Warning: Requesting number of tracks that is greater than 10. Trimming results to " +
                                    "" + from + "-" + (from + 9) +" :exclamation:").queue();
                            to = from + 9;
                        }
                        String msg = "Added " + (to - from + 1) + " songs to queue: ```";
                        int count = 1;
                        for (int i = from - 1; i < to; i++) {
                            play(channel.getGuild(), musicManager, playlist.getTracks().get(i), author);
                            msg += count + ": " +  playlist.getTracks().get(i).getInfo().title + "\n";
                            count++;
                        }
                        msg += "```";
                        channel.sendMessage(msg).queue();
                    } else {
                        channel.sendMessage(":x: Error: Incorrect number of parameters. Make sure that there are no spaces between your track numbers and the dash :x:").queue();
                    }
                }
            }

            @Override
            public void noMatches() {
                channel.sendMessage("Nothing found by " + trackUrl).queue();
            }

            @Override
            public void loadFailed(FriendlyException exception) {
                channel.sendMessage("Could not play: " + exception.getMessage()).queue();
            }
        });
    }

    private void play(Guild guild, ServerMusicManager musicManager, AudioTrack track, final Member author) {
        connectToVoiceChannel(guild.getAudioManager(), author);

        musicManager.scheduler.queue(track);
    }

    private void skipTrack(TextChannel channel) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(channel.getGuild().getId()));
        if (musicManager == null) {
            channel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        musicManager.scheduler.nextTrack();

        channel.sendMessage("Skipped to next track.").queue();
    }

    private static void connectToVoiceChannel(AudioManager audioManager, final Member author) {
        if (!audioManager.isConnected() && !audioManager.isAttemptingToConnect()) {
            audioManager.openAudioConnection(author.getVoiceState().getChannel());
        }
    }

    private void pauseTrack(final TextChannel textChannel) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(textChannel.getGuild().getId()));
        if (musicManager == null) {
            textChannel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio").queue();
            return;
        }
        musicManager.scheduler.pause();
        textChannel.sendMessage("Successfully paused stream").queue();
    }

    private void resumeTrack(final TextChannel textChannel) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(textChannel.getGuild().getId()));
        if (musicManager == null) {
            textChannel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio").queue();
            return;
        }
        musicManager.scheduler.resume();
        textChannel.sendMessage("Successfully resumed Stream").queue();
    }

    private void stopPlayer(final TextChannel textChannel) {
        long guildId = Long.parseLong(textChannel.getGuild().getId());
        ServerMusicManager musicManager = musicManagers.get(guildId);
        if (musicManager == null) {
            textChannel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio").queue();
            return;
        }
        musicManager.scheduler.stopPlayer();
        textChannel.getGuild().getAudioManager().closeAudioConnection();
        textChannel.sendMessage("Stopping player").queue();
        musicManagers.put(guildId, null);
        System.out.println(musicManagers.size());
        musicManagers.remove(guildId);
        System.out.println(musicManagers.size());
        System.gc();
    }

    private void getPlaylist(final TextChannel textChannel) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(textChannel.getGuild().getId()));
        if (musicManager == null) {
            textChannel.sendMessage("There is currently no audio playing.").queue();
            return;
        }
        if (!musicManager.scheduler.isPlaying()) {
            textChannel.sendMessage("You are not listening to audio").queue();
            return;
        } else {
            String[] playlist = musicManager.scheduler.getPlaylist();
            String msg = "```Playlist\n";
            for (int i = 0; i < playlist.length; i++) {
                if (i == 0)
                    msg += "Now Playing: " + playlist[i] + "\n";
                else if (i == 1) {
                    msg += "Next: " + playlist[i] + "\n";
                } else
                    msg += (i + 1) + ": " + playlist[i] + "\n";
            }
            msg += "```";
            textChannel.sendMessage(msg).queue();
        }
    }

    private int getNumberActiveStreams() {
        int count = 0;
        for (Map.Entry<Long, ServerMusicManager> entry : musicManagers.entrySet()) {
            ServerMusicManager manager = entry.getValue();
            if (manager.scheduler.isPlaying()) {
                count++;
            }
        }
        return count;
    }

    private void voiceStats(TextChannel textChannel) {
        int activeServers = getNumberActiveStreams();
        int totalServers = musicManagers.size();
        String mem = (((Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory()) / 1024) / 1024) + " MB";
        EmbedBuilder builder = new EmbedBuilder();
        builder.setAuthor(nickName, avatarURL, avatarURL);
        builder.addField("Total voice servers", "" + totalServers, true);
        builder.addField("Active voice servers", "" + activeServers, true);
        builder.addField("Memory used", "" + mem, true);
        textChannel.sendMessage(builder.build()).queue();
    }


    private void search(final TextChannel channel, final String trackUrl, final Member author) {
        final ServerMusicManager musicManager = getServerAudioPlayer(channel.getGuild());

        playerManager.loadItemOrdered(channel.getGuild(), "ytsearch:" + trackUrl, new AudioLoadResultHandler() {
            @Override
            public void trackLoaded(AudioTrack track) {
                channel.sendMessage("Adding to queue " + track.getInfo().title).queue();

                play(channel.getGuild(), musicManager, track, author);
            }

            @Override
            public void playlistLoaded(AudioPlaylist playlist) {
                System.out.print("here: " + playlist.getTracks().size());
                EmbedBuilder builder = new EmbedBuilder();

                builder.setAuthor(nickName, avatarURL, avatarURL);
                builder.addField("Select a song to add by reacting with the corresponding number", "", false);
                for (int i = 0; i < playlist.getTracks().size(); i++) {
                    builder.addField("", i + ": " + playlist.getTracks().get(i).getInfo().title, false);
                    //System.out.print("Track");
                }
                channel.sendMessage(builder.build()).queue();
            }

            @Override
            public void noMatches() {
                channel.sendMessage("Nothing found for " + trackUrl).queue();
            }

            @Override
            public void loadFailed(FriendlyException exception) {
                channel.sendMessage("Could not play: " + exception.getMessage()).queue();
            }
        });
    }

    private void checkVoiceLobby(Guild guild) {
        ServerMusicManager musicManager = musicManagers.get(Long.parseLong(guild.getId()));
        if (musicManager == null) {
            return;
        } else if (guild.getAudioManager().isConnected()) {
            if (guild.getAudioManager().getConnectedChannel().getMembers().size() == 1) {
                long guildId = Long.parseLong(guild.getId());
                musicManager.scheduler.stopPlayer();
                guild.getAudioManager().closeAudioConnection();
                System.out.println(musicManagers.remove(guildId));
                System.out.print(musicManagers.size());
                System.gc();
            }
        }

    }


}