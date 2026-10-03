import React, { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import {
  MessageSquare,
  Send,
  Calendar,
  CheckCircle,
  XCircle,
  Building,
  User,
  Clock,
  ArrowLeft,
  ShieldCheck,
  AlertCircle,
  Flag,
} from 'lucide-react'
import { useAuthStore } from '../../store/authStore'
import { messagingService } from '../../services/messagingService'
import { formatCurrency } from '../../lib/utils'
import { ReportUserModal } from '../../components/reports/ReportUserModal'

export const Chat = () => {
  const { conversationId } = useParams()
  const navigate = useNavigate()
  const { user } = useAuthStore()

  const [conversations, setConversations] = useState([])
  const [activeConv, setActiveConv] = useState(null)
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [loading, setLoading] = useState(true)
  const [messagesLoading, setMessagesLoading] = useState(false)
  const [sending, setSending] = useState(false)
  const [wsConnected, setWsConnected] = useState(false)
  const [isReportModalOpen, setIsReportModalOpen] = useState(false)

  const messagesEndRef = useRef(null)
  const wsRef = useRef(null)

  // Fetch all conversations
  useEffect(() => {
    loadConversations()
  }, [])

  // Auto-select conversation or load route conversation
  useEffect(() => {
    if (conversationId && conversations.length > 0) {
      const found = conversations.find((c) => c.id === conversationId)
      if (found) {
        selectConversation(found)
      } else {
        // Load direct by ID if not yet in list
        loadSingleConversation(conversationId)
      }
    } else if (!conversationId && conversations.length > 0 && !activeConv) {
      selectConversation(conversations[0])
    }
  }, [conversationId, conversations])

  // Setup WebSocket when active conversation changes
  useEffect(() => {
    if (!activeConv) return

    loadMessages(activeConv.id)

    // Connect WebSocket
    const wsUrl = messagingService.getWebSocketUrl(activeConv.id)
    const ws = new WebSocket(wsUrl)
    wsRef.current = ws

    ws.onopen = () => {
      setWsConnected(true)
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'NEW_MESSAGE' && data.message) {
          setMessages((prev) => {
            // Avoid duplicate message if already added optimistically
            if (prev.some((m) => m.id === data.message.id)) return prev
            return [...prev, data.message]
          })
          // Mark read
          messagingService.markAsRead(activeConv.id).catch(() => {})
        } else if (data.type === 'MESSAGES_READ') {
          setMessages((prev) =>
            prev.map((m) => (m.sender_id === user?.id ? { ...m, is_read: true } : m))
          )
        }
      } catch (err) {
        console.error('WS parse error:', err)
      }
    }

    ws.onclose = () => {
      setWsConnected(false)
    }

    ws.onerror = (err) => {
      console.warn('WS error:', err)
      setWsConnected(false)
    }

    return () => {
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close()
      }
    }
  }, [activeConv?.id])

  // Auto-scroll messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const loadConversations = async () => {
    try {
      setLoading(true)
      const data = await messagingService.getConversations()
      setConversations(data)
    } catch (err) {
      console.error('Failed to load conversations:', err)
    } finally {
      setLoading(false)
    }
  }

  const loadSingleConversation = async (id) => {
    try {
      const data = await messagingService.getConversation(id)
      setActiveConv(data)
    } catch (err) {
      console.error('Failed to load conversation:', err)
    }
  }

  const loadMessages = async (convId) => {
    try {
      setMessagesLoading(true)
      const data = await messagingService.getMessages(convId)
      setMessages(data)
      await messagingService.markAsRead(convId)
      // Clear unread count locally in sidebar
      setConversations((prev) =>
        prev.map((c) => (c.id === convId ? { ...c, unread_count: 0 } : c))
      )
    } catch (err) {
      console.error('Failed to load messages:', err)
    } finally {
      setMessagesLoading(false)
    }
  }

  const selectConversation = (conv) => {
    setActiveConv(conv)
    navigate(`/messages/${conv.id}`, { replace: true })
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!newMessage.trim() || !activeConv || sending) return

    const content = newMessage.trim()
    setNewMessage('')
    setSending(true)

    // Try sending via WebSocket first for sub-millisecond delivery
    let sentViaWs = false
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      try {
        wsRef.current.send(JSON.stringify({ action: 'SEND_MESSAGE', content }))
        sentViaWs = true
      } catch (err) {
        console.warn('WS send failed, falling back to HTTP', err)
      }
    }

    if (!sentViaWs) {
      try {
        const msg = await messagingService.sendMessage(activeConv.id, { content, message_type: 'TEXT' })
        setMessages((prev) => [...prev, msg])
      } catch (err) {
        console.error('Failed to send message:', err)
      }
    }

    setSending(false)
  }

  const getCounterpart = (conv) => {
    if (!conv || !user) return null
    return user.id === conv.student_id ? conv.landlord : conv.student
  }

  const counterpart = getCounterpart(activeConv)

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div className="bg-white rounded-2xl border border-neutral-200 shadow-sm overflow-hidden flex flex-col md:flex-row h-[780px]">
        {/* Left Sidebar: Conversations Inbox */}
        <div
          className={`w-full md:w-80 lg:w-96 border-r border-neutral-200 flex flex-col ${
            activeConv ? 'hidden md:flex' : 'flex'
          }`}
        >
          <div className="p-4 border-b border-neutral-200 bg-neutral-50/50 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageSquare className="text-primary" size={20} />
              <h2 className="font-heading font-bold text-neutral-900 text-lg">Inbox</h2>
            </div>
            <span className="text-xs px-2.5 py-1 bg-primary/10 text-primary font-semibold rounded-full">
              {conversations.length} {conversations.length === 1 ? 'chat' : 'chats'}
            </span>
          </div>

          <div className="flex-1 overflow-y-auto divide-y divide-neutral-100">
            {loading ? (
              <div className="p-8 text-center text-neutral-400 text-sm">Loading conversations...</div>
            ) : conversations.length === 0 ? (
              <div className="p-8 text-center text-neutral-500 space-y-3">
                <MessageSquare className="mx-auto text-neutral-300" size={36} />
                <p className="text-sm font-medium text-neutral-700">No conversations yet</p>
                <p className="text-xs text-neutral-400">
                  When you inquire about a property or receive an inquiry, chats will appear here.
                </p>
                <Link
                  to="/search"
                  className="inline-block mt-2 px-4 py-2 bg-primary text-white text-xs font-semibold rounded-xl hover:bg-primary-dark transition"
                >
                  Browse Listings
                </Link>
              </div>
            ) : (
              conversations.map((conv) => {
                const other = getCounterpart(conv)
                const isSelected = activeConv?.id === conv.id
                return (
                  <button
                    key={conv.id}
                    onClick={() => selectConversation(conv)}
                    className={`w-full text-left p-4 transition-colors flex items-start gap-3 hover:bg-neutral-50 ${
                      isSelected ? 'bg-primary/5 border-l-4 border-primary' : ''
                    }`}
                  >
                    <div className="w-11 h-11 rounded-full bg-gradient-to-tr from-primary to-primary-light text-white font-bold flex items-center justify-center shrink-0 text-sm shadow-sm">
                      {other?.full_name?.charAt(0) || 'U'}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-semibold text-sm text-neutral-900 truncate">
                          {other?.full_name || 'User'}
                        </span>
                        <span className="text-[10px] text-neutral-400 shrink-0">
                          {conv.last_message?.created_at
                            ? new Date(conv.last_message.created_at).toLocaleDateString([], {
                                month: 'short',
                                day: 'numeric',
                              })
                            : ''}
                        </span>
                      </div>

                      {conv.listing && (
                        <div className="flex items-center gap-1 text-xs text-primary font-medium mb-1 truncate">
                          <Building size={12} className="shrink-0" />
                          <span className="truncate">{conv.listing.title}</span>
                        </div>
                      )}

                      <div className="flex items-center justify-between gap-2">
                        <p className="text-xs text-neutral-500 truncate">
                          {conv.last_message?.content || 'No messages yet'}
                        </p>
                        {conv.unread_count > 0 && (
                          <span className="w-5 h-5 bg-primary text-white text-[11px] font-bold rounded-full flex items-center justify-center shrink-0">
                            {conv.unread_count}
                          </span>
                        )}
                      </div>
                    </div>
                  </button>
                )
              })
            )}
          </div>
        </div>

        {/* Right Area: Active Chat Thread */}
        <div
          className={`flex-1 flex flex-col bg-neutral-50/30 ${
            !activeConv ? 'hidden md:flex' : 'flex'
          }`}
        >
          {activeConv ? (
            <>
              {/* Chat Header */}
              <div className="p-4 bg-white border-b border-neutral-200 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => setActiveConv(null)}
                    className="md:hidden p-1.5 text-neutral-500 hover:text-neutral-900 rounded-lg hover:bg-neutral-100"
                  >
                    <ArrowLeft size={18} />
                  </button>

                  <div className="w-10 h-10 rounded-full bg-primary/10 text-primary font-bold flex items-center justify-center shrink-0">
                    {counterpart?.full_name?.charAt(0) || 'U'}
                  </div>

                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-neutral-900 text-sm">
                        {counterpart?.full_name || 'Participant'}
                      </h3>
                      <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-neutral-100 text-neutral-600">
                        {counterpart?.role}
                      </span>
                      {wsConnected && (
                        <span className="flex items-center gap-1 text-[11px] text-emerald-600 font-medium">
                          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                          Live
                        </span>
                      )}
                    </div>
                    {activeConv.listing && (
                      <Link
                        to={`/listings/${activeConv.listing.id}`}
                        className="text-xs text-primary hover:underline inline-flex items-center gap-1"
                      >
                        <Building size={11} />
                        {activeConv.listing.title} • {formatCurrency(activeConv.listing.rent_amount)}/mo
                      </Link>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  {/* Quick Action: Booking Status */}
                  {user?.role === 'STUDENT' ? (
                    <Link
                      to="/bookings"
                      className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 bg-neutral-100 hover:bg-neutral-200 text-neutral-700 text-xs font-semibold rounded-xl transition"
                    >
                      <Calendar size={13} />
                      My Bookings
                    </Link>
                  ) : (
                    <Link
                      to="/landlord/bookings"
                      className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 bg-neutral-100 hover:bg-neutral-200 text-neutral-700 text-xs font-semibold rounded-xl transition"
                    >
                      <Calendar size={13} />
                      Manage Requests
                    </Link>
                  )}

                  {/* Report User Action */}
                  {counterpart && (!user || user.id !== counterpart.id) && (
                    <button
                      type="button"
                      onClick={() => setIsReportModalOpen(true)}
                      className="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium text-neutral-500 hover:text-red-600 hover:bg-red-50 rounded-xl transition border border-neutral-200 hover:border-red-200"
                      title={`Report ${counterpart.full_name} for inappropriate behaviour`}
                    >
                      <Flag size={13} />
                      <span className="hidden sm:inline">Report</span>
                    </button>
                  )}
                </div>
              </div>

              {/* Messages Body */}
              <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {messagesLoading ? (
                  <div className="text-center py-10 text-neutral-400 text-xs">Loading message history...</div>
                ) : messages.length === 0 ? (
                  <div className="text-center py-12 text-neutral-400 space-y-2">
                    <MessageSquare className="mx-auto text-neutral-300" size={32} />
                    <p className="text-xs font-medium">Start the conversation with {counterpart?.full_name}</p>
                  </div>
                ) : (
                  messages.map((msg) => {
                    const isMe = msg.sender_id === user?.id
                    const isSystem = msg.message_type === 'SYSTEM'

                    if (isSystem) {
                      return (
                        <div key={msg.id} className="flex justify-center my-4">
                          <div className="max-w-md bg-white border border-primary/20 rounded-2xl p-3 text-xs text-neutral-700 shadow-sm space-y-1">
                            <div className="flex items-center gap-1.5 text-primary font-semibold">
                              <ShieldCheck size={14} />
                              <span>NestMatch Update</span>
                            </div>
                            <p className="whitespace-pre-line leading-relaxed">{msg.content}</p>
                            <span className="text-[10px] text-neutral-400 block text-right">
                              {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </span>
                          </div>
                        </div>
                      )
                    }

                    return (
                      <div
                        key={msg.id}
                        className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}
                      >
                        <div
                          className={`max-w-[75%] sm:max-w-md px-4 py-2.5 rounded-2xl text-sm leading-relaxed shadow-sm ${
                            isMe
                              ? 'bg-primary text-white rounded-br-none'
                              : 'bg-white text-neutral-900 border border-neutral-200 rounded-bl-none'
                          }`}
                        >
                          <p className="whitespace-pre-line">{msg.content}</p>
                          <div
                            className={`flex items-center justify-end gap-1 mt-1 text-[10px] ${
                              isMe ? 'text-white/80' : 'text-neutral-400'
                            }`}
                          >
                            <span>
                              {new Date(msg.created_at).toLocaleTimeString([], {
                                hour: '2-digit',
                                minute: '2-digit',
                              })}
                            </span>
                            {isMe && (
                              <span>
                                {msg.is_read ? '✓✓' : '✓'}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    )
                  })
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Message Input Bar */}
              <div className="p-3 bg-white border-t border-neutral-200">
                <form onSubmit={handleSendMessage} className="flex items-center gap-2">
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    placeholder="Type your message..."
                    className="flex-1 px-4 py-2.5 bg-neutral-50 border border-neutral-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition"
                  />
                  <button
                    type="submit"
                    disabled={!newMessage.trim() || sending}
                    className="px-4 py-2.5 bg-primary hover:bg-primary-dark disabled:opacity-50 text-white rounded-xl text-sm font-semibold transition flex items-center justify-center gap-1.5 shadow-sm"
                  >
                    <Send size={15} />
                    <span className="hidden sm:inline">Send</span>
                  </button>
                </form>
              </div>
            </>
          ) : (
            <div className="flex-1 flex flex-col items-center justify-center p-8 text-center text-neutral-400">
              <MessageSquare size={48} className="text-neutral-300 mb-3" />
              <p className="font-semibold text-neutral-700 text-base">Select a conversation</p>
              <p className="text-xs text-neutral-400 max-w-sm mt-1">
                Choose an existing chat from the left panel or enquire on any listing to start communicating.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Report User Modal */}
      {counterpart && (
        <ReportUserModal
          isOpen={isReportModalOpen}
          onClose={() => setIsReportModalOpen(false)}
          reportedUser={counterpart}
          contextType={counterpart.role === 'LANDLORD' ? 'landlord' : 'student'}
          listingTitle={activeConv?.listing?.title}
        />
      )}
    </div>
  )
}

export default Chat
