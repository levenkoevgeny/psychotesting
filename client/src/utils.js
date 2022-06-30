export const getLocalToken = () => localStorage.getItem("token")
export const getLocalUserId = () => localStorage.getItem("userId")

export const saveLocalToken = (token) => localStorage.setItem("token", token)
export const saveLocalUserId = (userId) =>
  localStorage.setItem("userId", userId)

export const removeLocalToken = () => localStorage.removeItem("token")
export const removeLocalUserId = () => localStorage.removeItem("userId")
